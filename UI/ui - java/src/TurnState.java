import java.util.ArrayList;
import java.util.List;

public class TurnState {

    List<Integer> player1Properties =  new ArrayList<>();
    List<Integer> player2Properties =  new ArrayList<>();

    List<Integer> player1Houses = new ArrayList<>();
    List<Integer> player2Houses = new ArrayList<>();

    List<Integer> player1JailCards;
    List<Integer> player2JailCards;

    List<Integer> player1Mortgaged = new ArrayList<>();
    List<Integer> player2Mortgaged = new ArrayList<>();

    int player1Cash;
    int player2Cash;

    int player1Position;
    int player2Position;

    @Override
    public String toString() {
        return "TurnState{" +
                "player1Properties=" + player1Properties +
                ", player2Properties=" + player2Properties +
                ", player1Houses=" + player1Houses +
                ", player2Houses=" + player2Houses +
                ", player1JailCards=" + player1JailCards +
                ", player2JailCards=" + player2JailCards +
                ", player1Mortgaged=" + player1Mortgaged +
                ", player2Mortgaged=" + player2Mortgaged +
                ", player1Cash=" + player1Cash +
                ", player2Cash=" + player2Cash +
                ", player1Position=" + player1Position +
                ", player2Position=" + player2Position +
                '}';
    }

    public void addProperty(int player, int property) {
        if (player == 1) {
            player1Properties.add(property);
        } else {
            player2Properties.add(property);
        }
    }

    public void addHouses(int player, int property) {
        if (player == 1) {
            player1Houses.add(property);
        } else {
            player2Houses.add(property);
        }
    }

    public void addMortgaged(int player, int property) {
        if (player == 1) {
            player1Mortgaged.add(property);
        } else {
            player2Mortgaged.add(property);
        }
    }
}
