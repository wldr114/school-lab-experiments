import java.util.Scanner;

interface WritingTool {
    void write();
}

// ================= 具体产品 =================

class Pen implements WritingTool {

    public void write() {
        System.out.println("钢笔书写：流畅书写文字");
    }
}

class BallPen implements WritingTool {

    public void write() {
        System.out.println("圆珠笔书写：日常记录文字");
    }
}

class BrushPen implements WritingTool {

    public void write() {
        System.out.println("毛笔书写：传统书法艺术");
    }
}

// ================= 抽象工厂 =================

interface WritingToolFactory {
    WritingTool createTool();
}

// ================= 具体工厂 =================

class PenFactory implements WritingToolFactory {

    public WritingTool createTool() {
        return new Pen();
    }
}

class BallPenFactory implements WritingToolFactory {

    public WritingTool createTool() {
        return new BallPen();
    }
}

class BrushPenFactory implements WritingToolFactory {

    public WritingTool createTool() {
        return new BrushPen();
    }
}

// ================= 测试类 =================

public class WritingToolFactorySystem {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("===== 书写工具工厂系统 =====");
        System.out.println("请选择书写工具类型：");
        System.out.println("  1 - 钢笔");
        System.out.println("  2 - 圆珠笔");
        System.out.println("  3 - 毛笔");
        System.out.println("  4 - 全部演示");
        System.out.print("请输入选择：");
        int choice = sc.nextInt();

        WritingToolFactory factory;

        switch (choice) {
            case 1:
                System.out.println("\n===钢笔工厂===");
                factory = new PenFactory();
                factory.createTool().write();
                break;
            case 2:
                System.out.println("\n===圆珠笔工厂===");
                factory = new BallPenFactory();
                factory.createTool().write();
                break;
            case 3:
                System.out.println("\n===毛笔工厂===");
                factory = new BrushPenFactory();
                factory.createTool().write();
                break;
            case 4:
                System.out.println("\n===钢笔工厂===");
                factory = new PenFactory();
                factory.createTool().write();

                System.out.println("\n===圆珠笔工厂===");
                factory = new BallPenFactory();
                factory.createTool().write();

                System.out.println("\n===毛笔工厂===");
                factory = new BrushPenFactory();
                factory.createTool().write();
                break;
            default:
                System.out.println("输入无效！");
        }

        sc.close();
    }
}