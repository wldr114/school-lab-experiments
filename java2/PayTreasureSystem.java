import java.util.ArrayList;
import java.util.Scanner;

class BankCard {

    private String id;
    private String name;
    private String password;
    private double balance;

    public BankCard(String id, String name, String password, double balance) {
        this.id = id;
        this.name = name;
        this.password = password;
        this.balance = balance;
    }

    public boolean verify(String pwd) {
        return this.password.equals(pwd);
    }

    public double getBalance() {
        return balance;
    }

    public String getName() {
        return name;
    }

    public double withdraw(double money) {
        double used = Math.min(balance, money);
        balance -= used;
        return used;
    }
}

class PayTreasure {

    private String password;
    private ArrayList<BankCard> cards = new ArrayList<>();

    public PayTreasure(String password) {
        this.password = password;
    }

    public void addCard(BankCard card, String pwd) {

        if (card.verify(pwd)) {
            cards.add(card);
            System.out.println(card.getName() + "银行卡绑定成功");
        } else {
            System.out.println("银行卡密码错误，绑定失败");
        }
    }

    public void pay(String merchant, double money, String pwd) {

        if (!this.password.equals(pwd)) {
            System.out.println("消费宝密码错误，支付失败");
            return;
        }

        double remain = money;

        System.out.println("向商家" + merchant + "支付" + money + "元，支付情况如下：");

        for (BankCard card : cards) {

            if (remain <= 0) break;

            double pay = card.withdraw(remain);
            remain -= pay;

            System.out.println(card.getName() +
                    "银行卡支付" + pay + "元，余额" + card.getBalance() + "元");
        }

        if (remain > 0) {
            System.out.println("余额不足，支付失败，还差：" + remain + "元");
        } else {
            System.out.println("支付成功");
        }
    }
}

public class PayTreasureSystem {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("===== 消费宝支付系统 =====");

        System.out.print("请设置消费宝支付密码：");
        String payPwd = sc.nextLine();
        PayTreasure pay = new PayTreasure(payPwd);
        System.out.println("消费宝注册成功！");

        System.out.print("请输入要绑定的银行卡数量：");
        int cardCount = sc.nextInt();
        sc.nextLine();

        for (int i = 0; i < cardCount; i++) {
            System.out.println("\n--- 绑定第" + (i + 1) + "张银行卡 ---");
            System.out.print("银行卡ID：");
            String id = sc.nextLine();
            System.out.print("银行名称：");
            String name = sc.nextLine();
            System.out.print("银行卡密码：");
            String cardPwd = sc.nextLine();
            System.out.print("银行卡余额：");
            double balance = sc.nextDouble();
            sc.nextLine();

            BankCard card = new BankCard(id, name, cardPwd, balance);
            pay.addCard(card, cardPwd);
        }

        System.out.print("\n是否进行支付？（y/n）：");
        String yn = sc.nextLine();
        if (yn.equalsIgnoreCase("y")) {
            System.out.print("商家名称：");
            String merchant = sc.nextLine();
            System.out.print("支付金额：");
            double money = sc.nextDouble();
            sc.nextLine();
            System.out.print("请输入消费宝支付密码：");
            String inputPwd = sc.nextLine();

            pay.pay(merchant, money, inputPwd);
        }

        System.out.println("感谢使用消费宝！");
        sc.close();
    }
}