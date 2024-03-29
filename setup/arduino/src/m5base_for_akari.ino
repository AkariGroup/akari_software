/*
  M5stack base soft for AKARI
  Created on 2020/05/08
  @author: Kazuya Yamamoto
*/

#include <ArduinoJson.h>
#include "Wire.h"
#include <M5Stack.h>
#include <M5GFX.h>
#include "M5UnitENV.h"
#include <WiFi.h>

const String m5_ver = "1.3.1";
const int boot_img_num = 48;

SemaphoreHandle_t xMutex = NULL;
M5GFX lcd;

//ピンアサイン
#define DIN0PIN 16
#define DIN1PIN 26
#define AIN0PIN 35
#define DOUT0PIN 5
#define DOUT1PIN 2
#define PWMOUT0PIN 17
#define LIGHTSENSORINPIN 36

bool isStart;
int seq = 0;
int PWMCH = 0;
unsigned long loopStart;
unsigned long loopEnd;
unsigned long interval;
#define LOOPPERIOD 20  //ループ周期をmsで定義
#define MEASURETIME 10 //1ループのinput測定回数
bool dout0Val;
bool dout1Val;
int pwmout0Val;
bool commandFlg = false;

QMP6988 qmp6988;
SHT4X sht4;
BMP280 bmp;

//Command number list
#define RESETPINVAL 0
#define WRITEPINVAL 1
#define FILLDISPLAY 10
#define DISPLAYSTRING 11
#define DISPLAYIMG 12
#define RESETM5 99
#define STARTM5 98

#define ENV_3 20
#define ENV_4 21
#define ENV_NONE 22
int connected_env_sensor = ENV_NONE;

float general0Val = 0.0F;
float general1Val = 0.0F;
#define FONTNUM  11
// SD内のフォントファイルパス。
const String fontList[FONTNUM] = {
    "MotoyaLMaru_18.vlw",
    "MotoyaLMaru_27.vlw",
    "MotoyaLMaru_36.vlw",
    "MotoyaLMaru_45.vlw",
    "MotoyaLMaru_54.vlw",
    "MotoyaLMaru_63.vlw",
    "MotoyaLMaru_72.vlw",
    "MotoyaLMaru_81.vlw",
    "MotoyaLMaru_90.vlw",
    "MotoyaLMaru_99.vlw",
    "MotoyaLMaru_108.vlw"};

int text_size = 0;
int fill_color = WHITE;
int text_color = BLACK;
int back_color = WHITE;
int req_x;
int req_y;
int req_fill_color;
int req_text_color;
int req_back_color;

//buttonの入力をMEASURETIME回の平均から決定(チャタリング対策)
bool buttonResult(int measure)
{
  if (measure >= MEASURETIME / 2)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

//dinの入力をMEASURETIME回の平均から決定(チャタリング対策)
bool dinResult(int measure)
{
  if (measure >= MEASURETIME / 2)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

//M5displayに表示するテキストの色、背景色を更新
void updateTextColor(int new_text_color, int new_back_color)
{
  if (new_text_color != -1)
    text_color = new_text_color;
  if (new_back_color != -1)
    back_color = new_back_color;
  else
    back_color = fill_color;
  lcd.setTextColor(text_color, back_color);
}

//日本語フォントのサイズ指示が変わった場合、対応するフォントをロードする。
void loadJapaneseFont(int size)
{
  String fontPath = "/Fonts/" + fontList[size - 1];
  lcd.loadFont(SD, fontPath.c_str());
}

//M5displayに表示するテキストのサイズを更新(1-7)
bool updateTextSize(int new_text_size)
{
  if (new_text_size < 1)
    return false;
  else if (new_text_size > FONTNUM)
    new_text_size = FONTNUM;
  if (new_text_size != text_size)
  {
    text_size = new_text_size;
    return true;
  }
  else
    return false;
}

//Serialでのコマンドを受信してJSONをパース、コマンドを実行する。
void subSerial(void *arg)
{
  BaseType_t xStatus;
  const TickType_t xTicksToWait = portMAX_DELAY;
  xSemaphoreGive(xMutex);
  while (1)
  {
    if (Serial.available() > 0)
    {
      String str;
      xStatus = xSemaphoreTake(xMutex, xTicksToWait);
      str = Serial.readStringUntil(';');
      StaticJsonDocument<300> rec;
      DeserializationError error = deserializeJson(rec, str);
      xSemaphoreGive(xMutex);
      if (error)
      {
        //Serial.print("deserializeJson() failed: ");
        //Serial.println(error.c_str());
      }
      else
      {
        switch ((int)rec["com"])
        {
        case RESETPINVAL:
          dout0Val = 0;
          dout1Val = 0;
          pwmout0Val = 0;
          digitalWrite(DOUT0PIN, rec["pin"]["do0"]);
          digitalWrite(DOUT1PIN, rec["pin"]["do1"]);
          ledcWrite(PWMCH, pwmout0Val);
          commandFlg = true;
          break;

        case WRITEPINVAL:
          dout0Val = rec["pin"]["do0"];
          dout1Val = rec["pin"]["do1"];
          pwmout0Val = rec["pin"]["po0"];
          digitalWrite(DOUT0PIN, rec["pin"]["do0"]);
          digitalWrite(DOUT1PIN, rec["pin"]["do1"]);
          ledcWrite(PWMCH, pwmout0Val);
          commandFlg = true;
          break;

        case FILLDISPLAY:
          req_fill_color = rec["lcd"]["cl"].as<int>();
          if (req_fill_color != -1)
            fill_color = req_fill_color;
          lcd.fillScreen(fill_color);
          commandFlg = true;
          break;

        case DISPLAYSTRING:
        {
          req_x = rec["lcd"]["x"].as<int>();
          req_y = rec["lcd"]["y"].as<int>();
          req_text_color = rec["lcd"]["cl"].as<int>();
          req_back_color = rec["lcd"]["bk"].as<int>();
          updateTextColor(req_text_color, req_back_color);
          if (updateTextSize(rec["lcd"]["sz"].as<int>()))
          {
            loadJapaneseFont(text_size);
          }
          if (rec["lcd"]["rf"].as<bool>())
          {
            lcd.fillScreen(fill_color);
          }
          //y位置のアライン
          if (req_y == -999)
          {
            req_y = lcd.height() / 2;
            if (req_x == -999)
            {
              lcd.setTextDatum(middle_center);
              req_x = lcd.width() / 2;
            }
            else if (req_x == 999)
            {
              lcd.setTextDatum(middle_right);
              req_x = lcd.width();
            }
            else
            {
              lcd.setTextDatum(middle_left);
            }
          }
          else if (req_y == 999)
          {
            req_y = lcd.height();
            if (req_x == -999)
            {
              lcd.setTextDatum(bottom_center);
              req_x = lcd.width() / 2;
            }
            else if (req_x == 999)
            {
              lcd.setTextDatum(bottom_right);
              req_x = lcd.width();
            }
            else
            {
              lcd.setTextDatum(bottom_left);
            }
          }
          else
          {
            if (req_x == -999)
            {
              lcd.setTextDatum(top_center);
              req_x = lcd.width() / 2;
            }
            else if (req_x == 999)
            {
              lcd.setTextDatum(top_right);
              req_x = lcd.width();
            }
            else
            {
              lcd.setTextDatum(top_left);
            }
          }
          lcd.drawString(rec["lcd"]["m"].as<String>(), req_x, req_y);
          commandFlg = true;
          break;
        }

        case DISPLAYIMG:
        {
          float req_scale = rec["lcd"]["scl"];
          if(req_scale < 0)
            req_scale = -1.0f;
          req_x = rec["lcd"]["x"].as<int>();
          req_y = rec["lcd"]["y"].as<int>();
          datum_t jpg_datum = top_left;

          //y位置のアライン
          if (req_y == -999)
          {
            req_y = 0;
            if (req_x == -999)
            {
              jpg_datum = datum_t::middle_center;
              req_x = 0;
            }
            else if (req_x == 999)
            {
              jpg_datum = datum_t::middle_right;
              req_x = 0;
            }
            else
            {
              jpg_datum = datum_t::middle_left;
            }
          }
          else if (req_y == 999)
          {
            req_y = 0;
            if (req_x == -999)
            {
              jpg_datum = datum_t::bottom_center;
              req_x = 0;
            }
            else if (req_x == 999)
            {
              jpg_datum = datum_t::bottom_right;
              req_x = 0;
            }
            else
            {
              jpg_datum = datum_t::bottom_left;
            }
          }
          else
          {
            if (req_x == -999)
            {
              jpg_datum = datum_t::top_center;
              req_x = 0;
            }
            else if (req_x == 999)
            {
              jpg_datum = datum_t::top_right;
              req_x = 0;
            }
            else
            {
              jpg_datum = datum_t::top_left;
            }
          }
          lcd.drawJpgFile(SD, rec["lcd"]["pth"].as<char *>(), req_x, req_y, lcd.width(), lcd.height(), 0, 0, req_scale, req_scale,jpg_datum);
          commandFlg = true;
          break;
        }

        case RESETM5:
          ESP.restart();

        default:
          break;
        }
      }
    }
    delay(100);
  }
  vTaskDelete(NULL);
}

//センサ、ioピンの値をJSON化して送信
void pubSerial(void *arg)
{
  BaseType_t xStatus;
  const TickType_t xTicksToWait = portMAX_DELAY;
  xSemaphoreGive(xMutex);
  while (1)
  {
    StaticJsonDocument<500> doc;
    int buttonAMeasure = 0;
    int buttonBMeasure = 0;
    int buttonCMeasure = 0;
    int din0Measure = 0;
    int din1Measure = 0;
    unsigned long ain0Measure = 0;
    //複数回計測して平均を返す
    for (int i = 0; i < MEASURETIME; i++)
    {
      buttonAMeasure += M5.BtnA.read();
      buttonBMeasure += M5.BtnB.read();
      buttonCMeasure += M5.BtnC.read();
      din0Measure += digitalRead(DIN0PIN);
      din1Measure += digitalRead(DIN1PIN);
      ain0Measure += analogRead(AIN0PIN);
    }
    float temperature = 0;
    float pressure = 0;
    float humidity = 0;
    if (connected_env_sensor == ENV_3) {
      qmp6988.update();
      temperature = (float)qmp6988.cTemp;
      pressure = (float)qmp6988.pressure;
    } else if (connected_env_sensor == ENV_4) {
      sht4.update();
      temperature = (float)sht4.cTemp;
      bmp.update();
      pressure = (float)bmp.pressure;
    }
    uint16_t brightness = analogRead(36);

    doc["seq"] = seq;
    doc["tmp"] = temperature;
    doc["pre"] = pressure;
    doc["bri"] = brightness;
    doc["btn"]["a"] = (int)buttonResult(buttonAMeasure);
    doc["btn"]["b"] = (int)buttonResult(buttonBMeasure);
    doc["btn"]["c"] = (int)buttonResult(buttonCMeasure);
    doc["io"]["di0"] = (int)dinResult(din0Measure);
    doc["io"]["di1"] = (int)dinResult(din1Measure);
    doc["io"]["ai0"] = (int)(ain0Measure / MEASURETIME);
    doc["io"]["do0"] = (int)dout0Val;
    doc["io"]["do1"] = (int)dout1Val;
    doc["io"]["po0"] = pwmout0Val;
    doc["io"]["gn0"] = (float)general0Val;
    doc["io"]["gn1"] = (float)general1Val;
    doc["co"] = (int)commandFlg;
    if(commandFlg){
      commandFlg = false;
    }
    xStatus = xSemaphoreTake(xMutex, xTicksToWait);
    serializeJson(doc, Serial);
    Serial.println();
    xSemaphoreGive(xMutex);
    seq++;
    loopEnd = millis();
    interval = loopEnd - loopStart;
    loopStart = loopEnd;
    if (interval < LOOPPERIOD)
    {
      delay(LOOPPERIOD - interval);
    }
  }
  vTaskDelete(NULL);
}

//起動待ち画面表示
void drawWaitingImg()
{
  lcd.drawJpgFile(SD, "/jpg/waiting.jpg");
  loadJapaneseFont(1);
  lcd.setTextColor(DARKGREY, BLACK);
  lcd.setTextDatum(bottom_left);
  lcd.drawString("ver:" + m5_ver, 0,  230);
  loadJapaneseFont(7);
  updateTextSize(7);
}

//起動アニメーション再生
void playBootAnime()
{
  for(int i=1;i<boot_img_num;i++){
    String fileName = "/jpg/boot/"+ String(i) +".jpg";
    char jpegs[fileName.length()+1];
    fileName.toCharArray(jpegs, sizeof(jpegs));
    lcd.drawJpgFile(SD,jpegs);
  }
}

void setup()
{
  M5.begin();
  M5.Power.begin();
  M5.Power.setPowerVin(false); //電源供給断時の自動再起動をOFFに
  WiFi.mode(WIFI_OFF);
  delay(500);
  M5.Lcd.setTextFont(2);
  lcd.begin();
  Wire.begin();
  lcd.setRotation(1);
  lcd.setBrightness(128);
  lcd.setColorDepth(24);
  drawWaitingImg();
  //接続されているENV_SENSORを判別
  if(bmp.begin(&Wire, BMP280_I2C_ADDR, 21, 22, 400000U) && (sht4.begin(&Wire, SHT40_I2C_ADDR_44, 21, 22, 400000U))){
      connected_env_sensor = ENV_4;
      sht4.setPrecision(SHT4X_HIGH_PRECISION);
      sht4.setHeater(SHT4X_NO_HEATER);
      bmp.setSampling(BMP280::MODE_NORMAL,
                      BMP280::SAMPLING_X2,
                      BMP280::SAMPLING_X16,
                      BMP280::FILTER_X16,
                      BMP280::STANDBY_MS_500);
    }
  }
  else if(qmp6988.begin(&Wire, QMP6988_SLAVE_ADDRESS_L, 21, 22, 400000U)) {
      connected_env_sensor = ENV_3;
  }
  dacWrite(25, 0); // Speaker OFF
  Serial.begin(500000);
  Serial.setTimeout(1);
  pinMode(DIN0PIN, INPUT_PULLUP);
  pinMode(DIN1PIN, INPUT_PULLUP);
  pinMode(AIN0PIN, INPUT);
  pinMode(LIGHTSENSORINPIN, INPUT);
  pinMode(DOUT0PIN, OUTPUT);
  pinMode(DOUT1PIN, OUTPUT);
  pinMode(PWMOUT0PIN, OUTPUT);
  ledcSetup(PWMCH, 7812.5, 8); //7812.5Hz, 8Bit(256段階)
  ledcAttachPin(PWMOUT0PIN, PWMCH);
  digitalWrite(DOUT0PIN, 0);
  digitalWrite(DOUT1PIN, 0);
  ledcWrite(PWMCH, 0);
  lcd.setTextColor(text_color, back_color);
  isStart = false;
  while (!isStart)
  {
    if (Serial.available() > 0)
    {
      String str;
      str = Serial.readStringUntil(';');
      StaticJsonDocument<300> rec;
      DeserializationError error = deserializeJson(rec, str);
      if (error)
      {
        //Serial.print("deserializeJson() failed: ");
        //Serial.println(error.c_str());
      }
      switch ((int)rec["com"])
      {
      case STARTM5:
        isStart = true;
        break;
      default:
        break;
      }
    }
    delay(1);
  }
  xMutex = xSemaphoreCreateMutex();
  playBootAnime();
  loopStart = millis();
  //esp32の各コアにタスク割当
  xTaskCreatePinnedToCore(pubSerial, "pubSerial", 8192, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(subSerial, "subSerial", 12288, NULL, 1, NULL, 1);
}

void loop()
{
  delay(1);
}
