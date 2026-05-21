import java.util.Scanner;

interface PCI {
    void start();
    void run();
    void stop();
}

class GraphicsCard implements PCI {

    public void start() {
        System.out.print("显卡启动 ");
    }

    public void run() {
        System.out.print("显卡运行 ");
    }

    public void stop() {
        System.out.print("显卡停止 ");
    }
}

class SoundCard implements PCI {

    public void start() {
        System.out.print("声卡启动 ");
    }

    public void run() {
        System.out.print("声卡运行 ");
    }

    public void stop() {
        System.out.print("声卡停止 ");
    }
}

class NetworkCard implements PCI {

    public void start() {
        System.out.print("网卡启动 ");
    }

    public void run() {
        System.out.print("网卡运行 ");
    }

    public void stop() {
        System.out.print("网卡停止 ");
    }
}

class MotherBoard {

    private PCI[] slots = new PCI[5];
    private int index = 0;

    public void install(PCI device) {
        if (index < slots.length) {
            slots[index++] = device;
        }
    }

    public void boot() {
        System.out.print("【开机】");
        for (int i = 0; i < index; i++) {
            slots[i].start();
        }
        for (int i = 0; i < index; i++) {
            slots[i].run();
        }
        System.out.println();
    }

    public void shutdown() {
        System.out.print("【关机】");
        for (int i = 0; i < index; i++) {
            slots[i].stop();
        }
        System.out.println();
    }
}

class Computer {

    private MotherBoard board = new MotherBoard();

    public void addDevice(PCI device) {
        board.install(device);
    }

    public void powerOn() {
        board.boot();
    }

    public void powerOff() {
        board.shutdown();
    }
}

public class MotherboardPCISystem {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("===== 主板PCI设备管理系统 =====");

        Computer computer = new Computer();

        System.out.println("请选择要安装的PCI设备（可多选，用空格分隔，输入0结束）：");
        System.out.println("  1 - 显卡");
        System.out.println("  2 - 声卡");
        System.out.println("  3 - 网卡");
        System.out.print("请输入选择：");

        String line = sc.nextLine();
        String[] choices = line.split("\\s+");

        for (String c : choices) {
            switch (c) {
                case "0":
                    break;
                case "1":
                    computer.addDevice(new GraphicsCard());
                    System.out.println("已安装显卡");
                    break;
                case "2":
                    computer.addDevice(new SoundCard());
                    System.out.println("已安装声卡");
                    break;
                case "3":
                    computer.addDevice(new NetworkCard());
                    System.out.println("已安装网卡");
                    break;
            }
        }

        System.out.print("\n是否开机演示？（y/n）：");
        String yn = sc.nextLine();
        if (yn.equalsIgnoreCase("y")) {
            computer.powerOn();
            computer.powerOff();
        }

        sc.close();
    }
}