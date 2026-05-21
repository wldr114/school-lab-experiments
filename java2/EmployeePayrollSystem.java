import java.util.Scanner;

abstract class Employee {
    protected String id;
    protected String name;
    protected int birthMonth;

    public Employee(String id, String name, int birthMonth) {
        this.id = id;
        this.name = name;
        this.birthMonth = birthMonth;
    }

    public abstract double earnings();

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getBirthMonth() {
        return birthMonth;
    }
}

class SalariedEmployee extends Employee {
    private double monthlySalary;

    public SalariedEmployee(String id, String name, int birthMonth, double monthlySalary) {
        super(id, name, birthMonth);
        this.monthlySalary = monthlySalary;
    }

    @Override
    public double earnings() {
        return monthlySalary;
    }
}

class HourlyEmployee extends Employee {
    private double wage;
    private int hours;

    public HourlyEmployee(String id, String name, int birthMonth, double wage, int hours) {
        super(id, name, birthMonth);
        this.wage = wage;
        this.hours = hours;
    }

    @Override
    public double earnings() {
        if (hours <= 160) {
            return wage * hours;
        } else {
            return 160 * wage + (hours - 160) * wage * 1.5;
        }
    }
}

class CommissionEmployee extends Employee {
    protected double sales;
    protected double rate;

    public CommissionEmployee(String id, String name, int birthMonth,
                                  double sales, double rate) {
        super(id, name, birthMonth);
        this.sales = sales;
        this.rate = rate;
    }

    @Override
    public double earnings() {
        return sales * rate;
    }
}

class BasePlusCommissionEmployee extends CommissionEmployee {
    private double baseSalary;

    public BasePlusCommissionEmployee(String id, String name,
                                          int birthMonth, double sales,
                                          double rate, double baseSalary) {
        super(id, name, birthMonth, sales, rate);
        this.baseSalary = baseSalary;
    }

    @Override
    public double earnings() {
        return baseSalary + sales * rate;
    }
}

public class EmployeePayrollSystem {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("===== 员工工资管理系统 =====");

        System.out.print("请输入公司名称：");
        String companyName = sc.nextLine();
        System.out.println("公司【" + companyName + "】工资管理启动~");

        System.out.print("请输入固定月薪员工的月薪：");
        double fixedSalary = sc.nextDouble();

        System.out.print("请输入当前月份（1-12）：");
        int currentMonth = sc.nextInt();

        System.out.print("请输入员工人数：");
        int count = sc.nextInt();
        sc.nextLine(); // 消耗换行

        Employee[] employees = new Employee[count];

        for (int i = 0; i < count; i++) {
            System.out.println("\n--- 录入第" + (i + 1) + "个员工 ---");
            System.out.print("请输入员工类型（1=固定月薪 2=小时工 3=佣金 4=底薪+佣金）：");
            int type = sc.nextInt();
            sc.nextLine();

            System.out.print("工号：");
            String id = sc.nextLine();
            System.out.print("姓名：");
            String name = sc.nextLine();
            System.out.print("出生月份（1-12）：");
            int birthMonth = sc.nextInt();

            switch (type) {
                case 1:
                    System.out.print("月薪（当前公司标准：" + fixedSalary + "元）：");
                    double ms = sc.nextDouble();
                    employees[i] = new SalariedEmployee(id, name, birthMonth, ms);
                    break;
                case 2:
                    System.out.print("时薪：");
                    double wage = sc.nextDouble();
                    System.out.print("工作小时数：");
                    int hours = sc.nextInt();
                    employees[i] = new HourlyEmployee(id, name, birthMonth, wage, hours);
                    break;
                case 3:
                    System.out.print("销售额：");
                    double sales = sc.nextDouble();
                    System.out.print("提成率（如0.05）：");
                    double rate = sc.nextDouble();
                    employees[i] = new CommissionEmployee(id, name, birthMonth, sales, rate);
                    break;
                case 4:
                    System.out.print("销售额：");
                    double sales2 = sc.nextDouble();
                    System.out.print("提成率（如0.04）：");
                    double rate2 = sc.nextDouble();
                    System.out.print("底薪：");
                    double base = sc.nextDouble();
                    employees[i] = new BasePlusCommissionEmployee(id, name, birthMonth, sales2, rate2, base);
                    break;
                default:
                    System.out.println("类型错误，默认创建固定月薪员工");
                    employees[i] = new SalariedEmployee(id, name, birthMonth, fixedSalary);
            }
            sc.nextLine(); // 消耗换行
        }

        System.out.println("\n===== " + companyName + " " + currentMonth + "月工资单 =====");
        for (Employee emp : employees) {
            double salary = emp.earnings();

            if (emp.getBirthMonth() == currentMonth) {
                salary += 100;
                System.out.println("  [生日月奖励100元]");
            }

            System.out.println("工号：" + emp.getId());
            System.out.println("姓名：" + emp.getName());
            System.out.println("出生月份：" + emp.getBirthMonth());
            System.out.println("月收入：" + salary);
            System.out.println("---------------------");
        }

        sc.close();
    }
}