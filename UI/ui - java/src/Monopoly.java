import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;

import static java.nio.file.Files.readAllBytes;

public class Monopoly {

    private static ArrayList<TurnState> gameState = new ArrayList<>();
    static ImageIcon p1_owned = new ImageIcon(getScaledImage("res/token1.png", 70, 70));
    static ImageIcon p2_owned = new ImageIcon(getScaledImage("res/token2.png", 70, 70));

    static ImageIcon p1_m = new ImageIcon(getScaledImage("res/p1_m.png", 70, 70));
    static ImageIcon p2_m = new ImageIcon(getScaledImage("res/p2_m.png", 70, 70));


    static {

        byte[] encoded = null;
        try {
            encoded = readAllBytes(Paths.get("log.json"));
            JSONObject jsonObject = new JSONObject(new String(encoded));
            JSONArray jsonArray = jsonObject.getJSONArray("states");

            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject turn = jsonArray.getJSONObject(i);

                TurnState turnState = new TurnState();
                turnState.player1Cash = turn.getInt("player_1_cash");
                turnState.player2Cash = turn.getInt("player_2_cash");

                turnState.player1Position = turn.getInt("player_1_pos");
                turnState.player2Position = turn.getInt("player_2_pos");

                JSONArray player1props = turn.getJSONArray("player_1_owned");
                JSONArray player2props = turn.getJSONArray("player_2_owned");
                JSONArray player1houses = turn.getJSONArray("player_1_houses");
                JSONArray player2houses = turn.getJSONArray("player_2_houses");
                JSONArray player1mort = turn.getJSONArray("player_1_mortgaged");
                JSONArray player2mort = turn.getJSONArray("player_2_mortgaged");

                for(int j = 0; j < player1props.length(); j++) {
                    turnState.addProperty(1, player1props.getInt(j));
                }

                for(int j = 0; j < player2props.length(); j++) {
                    turnState.addProperty(2, player2props.getInt(j));
                }

                for(int j = 0; j < player1houses.length(); j++) {
                    turnState.addHouses(1, player1houses.getInt(j));
                }

                for(int j = 0; j < player2houses.length(); j++) {
                    turnState.addHouses(2, player2houses.getInt(j));
                }

                for(int j = 0; j < player1mort.length(); j++) {
                    turnState.addMortgaged(1, player1mort.getInt(j));
                }

                for(int j = 0; j < player2mort.length(); j++) {
                    turnState.addMortgaged(2, player2mort.getInt(j));
                }

                System.out.println(turnState);
                gameState.add(turnState);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private JPanel board_main;

    private JLabel label_20;
    private JLabel label_0;
    private JLabel label_30;
    private JLabel label_10;
    private JLabel label_22;
    private JLabel label_25;
    private JLabel label_28;
    private JLabel label_17;
    private JLabel label_15;
    private JLabel label_12;
    private JLabel label_7;
    private JLabel label_5;
    private JLabel label_4;
    private JLabel label_36;
    private JLabel label_33;
    private JLabel label_35;
    private JLabel label_38;
    private JLabel label_2;

    private JTextField tf_tunCount;
    private JButton btn_setTurn;

    private JLabel label_21;
    private JLabel label_1;
    private JLabel label_3;
    private JLabel label_6;
    private JLabel label_9;
    private JLabel label_8;
    private JPanel board_3;
    private JLabel label_11;
    private JLabel label_13;
    private JLabel label_14;
    private JLabel label_16;
    private JLabel label_18;
    private JLabel label_19;
    private JLabel label_23;
    private JLabel label_24;
    private JLabel label_26;
    private JLabel label_27;
    private JLabel label_29;
    private JLabel label_31;
    private JLabel label_32;
    private JLabel label_34;
    private JLabel label_37;
    private JLabel label_39;

    private JLabel own_1;
    private JLabel own_9;
    private JLabel own_8;
    private JLabel own_6;
    private JLabel own_3;
    private JLabel own_39;
    private JLabel own_11;
    private JLabel own_13;
    private JLabel own_37;
    private JLabel own_14;
    private JLabel own_31;
    private JLabel own_32;
    private JLabel own_34;
    private JLabel own_19;
    private JLabel own_18;
    private JLabel own_16;
    private JLabel own_29;
    private JLabel own_27;
    private JLabel own_26;
    private JLabel own_24;
    private JLabel own_23;
    private JLabel own_21;
    private JLabel label_p1_cash;
    private JLabel label_p2_cash;
    private JLabel label_p1_position;
    private JLabel label_p2_position;

    private JLabel[] labels = {label_0, label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8, label_9, label_10, label_11, label_12, label_13, label_14, label_15, label_16, label_17, label_18,
            label_19, label_20, label_21, label_22, label_23, label_24, label_25, label_26, label_27, label_28, label_29, label_30, label_31, label_32, label_33, label_34, label_35, label_36, label_37, label_38, label_39};

    private JLabel[] ownerships = {null, own_1, null, own_3, null, label_5, own_6, null, own_8, own_9, null, own_11, null, own_13, own_14, label_15, own_16, null, own_18, own_19,
    null, own_21, null, own_23, own_24, label_25, own_26, own_27, label_28, own_29, null, own_31, own_32, null, own_34, label_35, null, own_37, null, own_39};

     Monopoly() {

        ImageIcon image20 = new ImageIcon(getScaledImage("res/topLeft.jpg", 90, 90));
        label_20.setIcon(image20);

        ImageIcon image10 = new ImageIcon(getScaledImage("res/bottomLeft.jpg", 90, 90));
        label_10.setIcon(image10);

        ImageIcon image30 = new ImageIcon(getScaledImage("res/topRight.jpg", 90, 90));
        label_30.setIcon(image30);

        ImageIcon image0 = new ImageIcon(getScaledImage("res/start.jpg", 90, 90));
        label_0.setIcon(image0);

        ImageIcon image22 = new ImageIcon(getScaledImage("res/top2.jpg", 70, 90));
        label_22.setIcon(image22);

        ImageIcon image25 = new ImageIcon(getScaledImage("res/top5.jpg", 70, 90));
        label_25.setIcon(image25);

        ImageIcon image28 = new ImageIcon(getScaledImage("res/top8.jpg", 70, 90));
        label_28.setIcon(image28);

        ImageIcon image8 = new ImageIcon(getScaledImage("res/bottom3.jpg", 70, 90));
        label_7.setIcon(image8);

        ImageIcon image5 = new ImageIcon(getScaledImage("res/bottom5.jpg", 70, 90));
        label_5.setIcon(image5);

        ImageIcon image4 = new ImageIcon(getScaledImage("res/bottom6.jpg", 70, 90));
        label_4.setIcon(image4);

        ImageIcon image36 = new ImageIcon(getScaledImage("res/right6.jpg", 90, 70));
        label_36.setIcon(image36);

        ImageIcon image32 = new ImageIcon(getScaledImage("res/right3.jpg", 90, 70));
        label_33.setIcon(image32);

        ImageIcon image35 = new ImageIcon(getScaledImage("res/right5.jpg", 90, 70));
        label_35.setIcon(image35);

        ImageIcon image38 = new ImageIcon(getScaledImage("res/right8.jpg", 90, 70));
        label_38.setIcon(image38);

        ImageIcon image17 = new ImageIcon(getScaledImage("res/left3.jpg", 90, 70));
        label_17.setIcon(image17);

        ImageIcon image15 = new ImageIcon(getScaledImage("res/left5.jpg", 90, 70));
        label_15.setIcon(image15);

        ImageIcon image12 = new ImageIcon(getScaledImage("res/left8.jpg", 90, 70));
        label_12.setIcon(image12);

        ImageIcon image2 = new ImageIcon(getScaledImage("res/bottom8.jpg", 70, 90));
        label_2.setIcon(image2);

        btn_setTurn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

//                if(!e.equals(ActionEvent.ACTION_PERFORMED)) return;

                String string = tf_tunCount.getText();
                int count = Integer.parseInt(string);

                if (count > gameState.size()) {
                    JOptionPane.showMessageDialog(btn_setTurn,"Invalid turn.");
                } else {

                    reset();
                    TurnState turnRequested = gameState.get(count);

                    label_p1_cash.setText("Player 1 cash : " + (turnRequested.player1Cash));
                    label_p2_cash.setText("Player 2 cash : " + (turnRequested.player2Cash));

                    label_p1_position.setText("Player 1 position : " + (turnRequested.player1Position));
                    label_p2_position.setText("Player 2 position : " + (turnRequested.player2Position));

                    for (int property : turnRequested.player1Houses) {

                        Integer i = Integer.parseInt(labels[property].getText());
                        labels[property].setText(String.valueOf(i+1));
                    }

                    for (int house : turnRequested.player2Houses) {

                        Integer i = Integer.parseInt(labels[house].getText());
                        labels[house].setText(String.valueOf(i+1));

                    }

                    for (int property : turnRequested.player1Properties) {
                        ownerships[property].setIcon(p1_owned);

                    }

                    for (int property : turnRequested.player2Properties) {
                        ownerships[property].setIcon(p2_owned);

                    }


                    for (int property : turnRequested.player1Mortgaged) {
                        ownerships[property].setIcon(p1_m);

                    }

                    for (int property : turnRequested.player2Mortgaged) {
                        ownerships[property].setIcon(p2_m);

                    }
                }
            }
        });
    }

    private void reset() {
        for (JLabel l : labels) {
            l.setText("0");
        }
    }

    private static Image getScaledImage(String path, int w, int h) {
        BufferedImage img = null;
        try {
            img = ImageIO.read(new File(path));
        } catch (IOException e) {
            e.printStackTrace();
        }

        Image dimg = img.getScaledInstance(w, h,
                Image.SCALE_SMOOTH);

        return dimg;
    }

    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            public void run() {

                JFrame frame = new JFrame("Monopoly");
                frame.setContentPane(new Monopoly().board_main);

                frame.setUndecorated(true);

                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

                frame.pack();
                frame.setResizable(true);

//                frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
//                frame.setUndecorated(true);

                frame.setVisible(true);

//                try {
//                    Monopoly window = new Monopoly();
//                    window.board_main.setVisible(true);
//                } catch (Exception e) {
//                    e.printStackTrace();
//                }
            }
        });
    }
}
