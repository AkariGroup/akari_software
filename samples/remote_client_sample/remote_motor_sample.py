#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from akari_client import AkariClient
from akari_client.config import (
    AkariClientConfig,
    JointManagerGrpcConfig,
    M5StackGrpcConfig,
)


def main() -> None:
    """
    メイン関数
    """
    # AKARI本体のIPアドレスを指定する。
    # 実際のAKARIのIPアドレスに合わせて変更すること。
    akari_ip = "192.168.100.1"
    # portは初期設定のままであれば51001固定
    akari_port = "51001"
    akari_endpoint = f"{akari_ip}:{akari_port}"

    joint_config: JointManagerGrpcConfig = JointManagerGrpcConfig(
        type="grpc", endpoint=akari_endpoint
    )
    m5_config: M5StackGrpcConfig = M5StackGrpcConfig(
        type="grpc", endpoint=akari_endpoint
    )
    akari_client_config = AkariClientConfig(
        joint_manager=joint_config, m5stack=m5_config
    )
    # akari_client_configを引数にしてAkariClientを作成する。
    try:
        akari = AkariClient(akari_client_config)
    except Exception as e:
        print(e)
        print("")
        print(
            "接続エラーです。AKARI本体が同一ネットワークに接続されていること、AkariRpcServerが起動していること、コード内のakari_ipをAKARI本体のIPアドレスに変更してください。"
        )
        return

    # 処理を記載。下記は例
    joints = akari.joints
    # STEP1.各軸の名前を取得し、表示する。
    print("STEP1. Get joint names")
    print(joints.get_joint_names())
    print("")
    time.sleep(3)

    # STEP2.サーボトルクをONする。
    print("STEP2. Servo torque ON")
    joints.enable_all_servo()
    print("")
    time.sleep(3)

    # STEP3.初期位置に移動する。"pan","tilt"それぞれの位置を0にしている。syncをTrueにすることで、移動完了まで待つ
    print("STEP3. Move to initial position. Wait until finish.")
    joints.move_joint_positions(sync=True, pan=0, tilt=0)
    print("")

    # STEP4.現在の軸の位置を表示。コマンドラインに表示される。
    print("STEP4. Get current joint position [rad]")
    print(joints.get_joint_positions())
    print("")
    time.sleep(3)

    # STEP5.panのモータだけ速度を3rad/sに変更する。
    print("STEP5. Set pan joint velocity at 3 rad/s")
    joints.set_joint_velocities(pan=3)
    print("")
    time.sleep(3)

    # STEP6.panのモータ位置だけを0.5[rad]に移動。
    print("STEP6. Move pan joint position to 0.5 rad")
    joints.move_joint_positions(sync=True, pan=0.5)
    print("")
    time.sleep(3)

    # STEP7.tiltのモータだけ速度を6rad/sに変更する。
    print("STEP7. Set tilt joint velocity at 6 rad/s")
    joints.set_joint_velocities(tilt=6)
    print("")
    time.sleep(3)

    # STEP8.tiltのモータ位置だけを0.5[rad]に移動。
    print("STEP8. Move tilt joint position to 0.5 rad")
    joints.move_joint_positions(tilt=0.5)
    print("")
    time.sleep(3)

    # STEP9.tiltのモータだけ加速度を1rad/sに変更する。
    print("STEP9. Set tilt joint accerelation at 1 rad/s")
    joints.set_joint_accelerations(tilt=1)
    print("")
    time.sleep(3)

    # STEP10.tiltのモータ位置だけを-0.4[rad]に移動。
    # syncをTrueにしていないため、移動完了前に次のコマンドが実行される。
    print("STEP10. Move tilt joint position to -0.4 rad")
    joints.move_joint_positions(tilt=-0.4)
    print("")
    time.sleep(0.5)

    # STEP11.panのモータ位置だけを-0.3[rad]に移動。
    # syncをTrueにしていないため、移動完了前に次のコマンドが実行される。
    print("STEP11. Move pan joint position to -0.3 rad")
    joints.move_joint_positions(pan=-0.3)
    print("")
    time.sleep(0.5)

    # STEP12.pan,tiltのモータ位置を(0.4, 0.4)[rad]に移動。syncをTrueにすることで、移動完了まで待つ
    print(
        "STEP12. Move pan joint position to 0.4 rad and tilt joint position to 0.4 rad. Wait until finish."
    )
    joints.move_joint_positions(sync=True, pan=0.4, tilt=0.4)
    print("")

    # STEP11.両方のモータ速度を10rad/sに変更。
    print("STEP13. Set both joints velocity at 10 rad/s")
    joints.set_joint_velocities(pan=10, tilt=10)
    print("")
    time.sleep(3)

    # STEP12.両方のモータ加速度を10rad/sに変更する。
    print("STEP14. Set both joints accerelation at 10 rad/s")
    joints.set_joint_accelerations(pan=10, tilt=10)
    print("")
    time.sleep(3)

    # STEP13.パンのモータ位置を-0.7,チルトのモータ位置を-0.3に移動。
    print(
        "STEP15. Move pan joint position to -0.7 rad and tilt joint position to -0.3 rad"
    )
    joints.move_joint_positions(pan=-0.7, tilt=-0.3)
    print("")
    time.sleep(3)

    # STEP14.現在の軸の位置を表示。コマンドラインに表示される。
    # [-0.7, 0.3]とほぼ一致していれば成功
    print("STEP16. Get current joint position [rad]")
    print(joints.get_joint_positions())
    print("")
    time.sleep(3)

    # STEP15.初期位置に戻る。
    print("STEP17. Return to initial position")
    joints.move_joint_positions(pan=0, tilt=0)
    print("")
    time.sleep(3)


if __name__ == "__main__":
    main()
