/*
  M5stack base soft for AKARI
  Created on 2020/05/08
  @author: Kazuya Yamamoto
*/

#include <ArduinoJson.h>
#include "Wire.h"
#include <M5Stack.h>
#include <M5GFX.h>
#include "UNIT_ENV.h"
#include <WiFi.h>
#include "AudioFileSourceSD.h"
#include "AudioFileSourceID3.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"

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

AudioGeneratorMP3* mp3;
AudioFileSourceSD* file;
AudioOutputI2S* out;
AudioFileSourceID3* id3;

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

//Command number list
#define RESETPINVAL 0
#define WRITEPINVAL 1
#define FILLDISPLAY 10
#define DISPLAYSTRING 11
#define DISPLAYIMG 12
#define PLAYMP3 13
#define STOPMP3 14
#define RESETM5 99
#define STARTM5 98

float general0Val = 0.0F;
float general1Val = 0.0F;

//SD内のフォントファイルパス。
const char *f18 = "Fonts/MotoyaLMaru_18";
const char *f36 = "Fonts/MotoyaLMaru_36";
const char *f54 = "Fonts/MotoyaLMaru_54";
const char *f72 = "Fonts/MotoyaLMaru_72";
const char *f90 = "Fonts/MotoyaLMaru_90";
const char *f108 = "Fonts/MotoyaLMaru_108";
const char *f126 = "Fonts/MotoyaLMaru_126";

int text_size = 0;
int fill_color = WHITE;
int text_color = BLACK;
int back_color = WHITE;
int req_x;
int req_y;
int req_fill_color;
int req_text_color;
int req_back_color;

bool mp3_stop_flg = false;

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

//M5displayに表示するテキストのサイズを更新(1-7)
bool updateTextSize(int new_text_size)
{
  if (new_text_size < 1)
    return false;
  else if (new_text_size > 7)
    new_text_size = 7;
  if (new_text_size != text_size)
  {
    text_size = new_text_size;
    return true;
  }
  else
    return false;
}

//日本語フォントのサイズ指示が変わった場合、対応するフォントをロードする。
void loadJapaneseFont(int size)
{
  switch (size)
  {
  case 1:
    lcd.loadFont(f18, SD);
    break;
  case 2:
    lcd.loadFont(f36, SD);
    break;
  case 3:
    lcd.loadFont(f54, SD);
    break;
  case 4:
    lcd.loadFont(f72, SD);
    break;
  case 5:
    lcd.loadFont(f90, SD);
    break;
  case 6:
    lcd.loadFont(f108, SD);
    break;
  case 7:
    lcd.loadFont(f126, SD);
    break;
  }
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
        
        case PLAYMP3:
          file = new AudioFileSourceSD(rec["mp3"]["pth"].as<char *>());
          id3 = new AudioFileSourceID3(file);
          out = new AudioOutputI2S(0, 1);  // Output to builtInDAC
          out->SetGain(0.3);
          out->SetOutputModeMono(true);
          mp3 = new AudioGeneratorMP3();
          mp3->begin(id3, out);
          commandFlg = true;
          break;

        case STOPMP3:
          mp3_stop_flg = true;
          commandFlg = true;
          break;

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
  if (mp3->isRunning()) {
    if (!mp3->loop() || mp3_stop_flg){
      mp3->stop();
      mp3_stop_flg = false;
    }
  }
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

    float temperature = (float)qmp6988.calcTemperature();
    float pressure = (float)qmp6988.calcPressure();
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

void setup()
{
  M5.begin();
  M5.Power.begin();
  M5.Power.setPowerVin(false); //電源供給断時の自動再起動をOFFに
  WiFi.mode(WIFI_OFF); 
  delay(500);

  M5.Lcd.setTextFont(2);
  M5.Lcd.printf("Sample MP3 playback begins...\n");
  Serial.printf("Sample MP3 playback begins...\n");
  lcd.begin();
  Wire.begin();
  lcd.setRotation(1);
  lcd.setBrightness(255);
  lcd.setColorDepth(24);
  lcd.drawJpgFile(SD, "/logo320_ex.jpg");
  qmp6988.init();
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
  lcd.loadFont(f18, SD);
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
  lcd.drawJpgFile(SD, "/logo320.jpg");
    delay(1);
  file = new AudioFileSourceSD("/booted.mp3");
  id3 = new AudioFileSourceID3(file);
  out = new AudioOutputI2S(0, 1);  // Output to builtInDAC
  out->SetGain(0.3);
  out->SetOutputModeMono(true);
  mp3 = new AudioGeneratorMP3();
  mp3->begin(id3, out);
  loopStart = millis();
  //esp32の各コアにタスク割当
  xTaskCreatePinnedToCore(pubSerial, "pubSerial", 8192, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(subSerial, "subSerial", 12288, NULL, 1, NULL, 1);
}

void loop()
{
  delay(1);
}
