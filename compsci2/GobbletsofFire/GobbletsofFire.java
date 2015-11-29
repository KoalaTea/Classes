/*
 * $Id: RJW4910.java,v 1.2 2014/03/11 03:35:58 rjw4910 Exp $
 * 
 * $Log: RJW4910.java,v $
 * Revision 1.2  2014/03/11 03:35:58  rjw4910
 * Finished
 *
 * Revision 1.1  2014/03/08 20:49:26  rjw4910
 * Just commiting for logs and what not.
 /


/**
 * 
 */

//COMMIT NOT WORK FOR THE TEAM ACCOUNT

package Players.GobbletsofFire;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Stack;

import utilities.Cloner;

import Engine.Logger;
import Interface.Coordinate;
import Interface.GobbletPart1;
import Interface.PlayerModule;
import Interface.PlayerMove;

/**
 * @author Ryan Whittier
 * @author Eric Kanis
 */
public class GobbletsofFire implements PlayerModule, GobbletPart1 {
	
	/**
	 * A class to hold piece data. Make things easier for me ya know.
	 * @author Ryan
	 *
	 */
	public static class Piece {
		private int pieceID;
		private int pieceSize;
		
		public Piece(int id, int size) {
			pieceID = id;
			pieceSize = size;
		}
		
		public int getId() {
			return pieceID;
		}
		public int getSize() {
			return pieceSize;
		}
	}
	
	private int myID;
	private Logger log;
	private Stack<Piece>[][] board = new Stack[4][4];
	private Stack<Piece>[] myStacks = new Stack[3];
	private Stack<Piece>[] oppStacks = new Stack[3];

	/**
	 * Initializes the player
	 * 
	 * @param arg1 - int of the player ID
	 * @param arg0 - I honestly don't know yet
	 */
	@Override
	public void init(Logger arg0, int arg1) {
		
		Cloner.addImmutable(Piece.class);
		myID = arg1;
		log = arg0;
		for(int i = 0; i < 4; i ++){
			for(int j = 0; j < 4; j++){
				board[i][j] = new Stack<Piece>();
			}
		}
		for(int i = 0; i< 3; i++){
			myStacks[i] = new Stack<>();
			for(int j = 1; j < 5; j++){
				myStacks[i].push(new Piece(myID, j));
			}
		}
		for(int i = 0; i< 3; i++){
			oppStacks[i] = new Stack<>();
			if(myID == 1){
				for(int j = 1; j < 5; j++){
					oppStacks[i].push(new Piece(2, j));
				}
			} else {
				for(int j = 1; j < 5; j++){
					oppStacks[i].push(new Piece(1, j));
				}
			}
		}
	}
	
	
	
	
	/**
	 * Creates the visual representation of the board and prints it.
	 */
	@Override
	public void dumpGameState() {
		
		// Goes through each row and adds spaces and [] if empty and size(id) if not empty
		String row0 = "";
		for(int i = 0; i < 4; i++){
			if(board[0][i].isEmpty()){
				row0 = row0 + "  [] ";
			} else {
				row0 = row0 + " " + board[0][i].peek().getSize() + "(" + board[0][i].peek().getId() + ")";
			}
		}
		String row1 = "";
		for(int i = 0; i < 4; i++){
			if(board[1][i].isEmpty()){
				row1 = row1 + "  [] ";
			} else {
				row1 = row1 + " " + board[1][i].peek().getSize() + "(" + board[1][i].peek().getId() + ")";
			}
		}
		String row2 = "";
		for(int i = 0; i < 4; i++){
			if(board[2][i].isEmpty()){
				row2 = row2 + "  [] ";
			} else {
				row2 = row2 + " " + board[2][i].peek().getSize() + "(" + board[2][i].peek().getId() + ")";
			}
		}
		String row3 = "";
		for(int i = 0; i < 4; i++){
			if(board[3][i].isEmpty()){
				row3 = row3 + "  [] ";
			} else {
				row3 = row3 + " " + board[3][i].peek().getSize() + "(" + board[3][i].peek().getId() + ")";
			}
		}
		// Create the player stacks representations and adds it to the row 1 and row 2
		String p1 = "   ";
		String p2 = "   ";
		if(myID == 1){
			for(int i = 0; i < 3; i++){
				if(myStacks[i].isEmpty()){
					p1 = p1 + "_ ";
				} else {
					p1 = p1 + myStacks[i].peek().getSize() + " ";
				}
				if(oppStacks[i].isEmpty()){
					p2 = p2 + "_ ";
				} else {
					p2 = p2 + oppStacks[i].peek().getSize() + " ";
				}
			}
		} else {
			for(int i = 0; i < 3; i++){
				if(oppStacks[i].isEmpty()){
					p1 = p1 + "_ ";
				} else {
					p1 = p1 + oppStacks[i].peek().getSize() + " ";
				}
				if(myStacks[i].isEmpty()){
					p2 = p2 + "_ ";
				} else {
					p2 = p2 + myStacks[i].peek().getSize() + " ";
				}
			}
		}
		row0 = row0 + p1;
		row2 = row2 + p2;
		System.out.println();
		System.out.println(row0);
		System.out.println(row1);
		System.out.println(row2);
		System.out.println(row3);
		System.out.println();
	}

	/**
	 * Returns the ID that my player holds.
	 */
	@Override
	public int getID() {
		// done.
		return myID;
	}

	/**
	 * Returns the ID of the top pieve at board[arg0][arg1]
	 * if empty return -1
	 * 
	 * @param arg0 - row
	 * @param arg1 - col
	 */
	@Override
	public int getTopOwnerOnBoard(int arg0, int arg1) {
		// done
		if(board[arg0][arg1].isEmpty()){
			return -1;
		} else {
			return board[arg0][arg1].peek().getId();
		}
	}

	/**
	 * Returns the size of the top piece at board[arg0][arg1]
	 * if empty return -1
	 * 
	 * @param arg0 - row
	 * @param arg1 - col
	 */
	@Override
	public int getTopSizeOnBoard(int arg0, int arg1) {
		// done
		if(board[arg0][arg1].isEmpty()){
			return -1;
		} else {
			return board[arg0][arg1].peek().getSize();
		}
	}

	/**
	 * returns the top size of the stack called. (if id matches mine, take it from my stack else
	 * look at top of oppstack. If empty return -1
	 * 
	 * @param arg0 - playerID
	 * @param arg1 - stack being looked at
	 */
	@Override
	public int getTopSizeOnStack(int arg0, int arg1) {
		// done
		int stackNum = (arg1 - 1);
		if(arg0 == myID){
			if(myStacks[stackNum].isEmpty()){
				return -1;
			} else {
				return myStacks[stackNum].peek().getSize();
			}
		} else {
			if(oppStacks[stackNum].isEmpty()){
				return -1;
			} else {
				return oppStacks[stackNum].peek().getSize();
			}
		}
	}


	/**
	 * moves a piece on the board to a new place or moves a piece from a stack onto the board.
	 * (the tracked board not the actual game board.)
	 * Already validated
	 * 
	 * @param arg0 - the move made being passed into my player.
	 */
	@Override
	public void lastMove(PlayerMove arg0) {
		// done
		if(arg0.getStack() == 0){
			int row = arg0.getStartRow();
			int col = arg0.getStartCol();
			Piece moved = board[row][col].pop();
			int row2 = arg0.getEndRow();
			int col2 = arg0.getEndCol();
			board[row2][col2].push(moved);
		} else {
			int stackNum = (arg0.getStack() - 1);
			if(arg0.getPlayerId() == myID){
				Piece moved = myStacks[stackNum].pop();
				int row = arg0.getEndRow();
				int col = arg0.getEndCol();
				board[row][col].push(moved);
			} else {
				Piece moved = oppStacks[stackNum].pop();
				int row = arg0.getEndRow();
				int col = arg0.getEndCol();
				board[row][col].push(moved);
			}
		}

	}
	
	
	@Override
	/**
	 * Makes a move to be returned using the function generateMoves
	 */
	public PlayerMove move() {
		List<PlayerMove> legalMoves = generateMoves(myID, board);
		PlayerMove ourMove = strategy(legalMoves);
		return ourMove;
	}
	
	/**
	 * Generates all legal moves using the isvalid to check
	 * 
	 * @param ID - the ID of the player moves are being made for
	 * @return a list of valid moves
	 */
	private List<PlayerMove> generateMoves(int ID, Stack<Piece>[][] usedBoard){
		List<PlayerMove> legalMoves = new ArrayList<PlayerMove>();
		int str = -1;
		int stc = -1;
		int size;
		for(int stack = 0; stack < myStacks.length; stack ++){
			if(ID == myID){
				if(!myStacks[stack].isEmpty()){
					size = myStacks[stack].peek().getSize();
					for(int er = 0; er < 4; er ++){
						for(int ec = 0; ec < 4; ec ++){
							Coordinate start = new Coordinate(str, stc);
							Coordinate end = new Coordinate(er, ec);
							PlayerMove theMove = new PlayerMove(ID, stack + 1, size, start, end);
							if(isValid(theMove, usedBoard)){
								legalMoves.add(theMove);
							}
						}
					}
				}
			} else {
				if(!oppStacks[stack].isEmpty()){
					size = oppStacks[stack].peek().getSize();
					for(int er = 0; er < 4; er ++){
						for(int ec = 0; ec < 4; ec ++){
							Coordinate start = new Coordinate(str, stc);
							Coordinate end = new Coordinate(er, ec);
							PlayerMove theMove = new PlayerMove(ID, stack + 1, size, start, end);
							if(isValid(theMove, usedBoard)){
								legalMoves.add(theMove);
							}
						}
					}
				}
			}
		}
		for(int sr = 0; sr < usedBoard.length; sr ++){
			for(int sc = 0; sc < usedBoard.length; sc ++){
				if(!usedBoard[sr][sc].isEmpty()){
					Coordinate start = new Coordinate(sr, sc);
					size = usedBoard[sr][sc].peek().getSize();
					for(int er = 0; er < usedBoard.length; er ++){
						for(int ec = 0; ec < usedBoard.length; ec ++){
							Coordinate end = new Coordinate(er, ec);
							PlayerMove theMove = new PlayerMove(ID, 0, size, start, end);
							if(isValid(theMove, usedBoard)){
								legalMoves.add(theMove);
							}
						}
					}
				}
			}
		}
		return legalMoves;
	}
	
	/**
	 * Checks for three in a row of opponents pieces for covering from the stack
	 * 
	 * @param row -row number
	 * @param col - col number
	 * @param ID - ID of player moving piece
	 * @return true if 3 of opp are there / false if not
	 */
	private boolean checkFor3(int row, int col, int ID, Stack<Piece>[][] usedBoard){
		int three = 0;
		if(row == col){
			for(int i = 0; i < 4; i++){
				if(!usedBoard[i][i].isEmpty()){
					if(usedBoard[i][i].peek().getId() != ID){
						three += 1;
					}
				}
			}
		}
		if(row + col == 3){
			for(int i = 0; i > 4; i++){
				if(!usedBoard[i][3-i].isEmpty()){
					if(usedBoard[i][3-i].peek().getId() != ID){
						three += 1;
					}
				}
			}
		}
		if(three == 3){
			return true;
		}
		three = 0;
		for(int r = 0; r < 4; r++){
			if(!usedBoard[r][col].isEmpty()){
				if(usedBoard[r][col].peek().getId() != ID){
					three += 1;
				}
			}
		}
		if(three == 3){
			return true;
		}
		three = 0;
		for(int c = 0; c < 4; c++){
			if(!usedBoard[row][c].isEmpty()){
				if(usedBoard[row][c].peek().getId() != ID){
					three += 1;
				}
			}
		}
		if(three == 3){
			return true;
		}
		return false;
	}
	
	/**
	 * Checks if a given move is valid.
	 * 
	 * @param move - the playermove object being checked
	 * @return true or false
	 */
	private boolean isValid(PlayerMove move, Stack<Piece>[][] usedBoard){
		int ID = move.getPlayerId();
		int endRow = move.getEndRow();
		int startRow = move.getStartRow();
		int endCol = move.getEndCol();
		int startCol = move.getStartCol();
		int stack = move.getStack() -1;
		int size = move.getSize();
		
		
		if(startRow == -1){
			if(startCol == -1){
				if(ID == myID){
					if(myStacks[stack].isEmpty()){
						return false;
					} else {
						if(myStacks[stack].peek().getSize() != size){
							return false;
						} else {
							if(usedBoard[endRow][endCol].isEmpty()){
								return true;
							} else if(usedBoard[endRow][endCol].peek().getSize() >= size){
								return false;
							} else {
								return checkFor3(endRow, endCol, ID, usedBoard);
							}
						}
					}
				} else {
					if(oppStacks[stack].isEmpty()){
						return false;
					} else {
						if(oppStacks[stack].peek().getSize() != size){
							return false;
						} else {
							if(usedBoard[endRow][endCol].isEmpty()){
								return true;
							} else if(usedBoard[endRow][endCol].peek().getSize() >= size){
								return false;
							} else {
								return checkFor3(endRow, endCol, ID, usedBoard);
							}
						}
					}
				}
			} 
		} else {
			if(stack + 1 != 0){
				return false;
			}
			if(startCol > -1){
				if(usedBoard[startRow][startCol].isEmpty()){
					return false;
				} else if(usedBoard[startRow][startCol].peek().getId() != ID){
					return false;
				} else if(usedBoard[startRow][startCol].peek().getSize() != size){
					return false;
				} else {
					if(usedBoard[endRow][endCol].isEmpty()){
						return true;
					} else if(usedBoard[endRow][endCol].peek().getSize() < 
							usedBoard[startRow][startCol].peek().getSize()){
						return true;
					} else {
						return false;
					}
				}
			}
		}
	return false;
	}
	
	
	private int threeLines(Stack<Piece>[][] checked){
		int score = 0;
		for(int r = 0; r<4; r++){
			if(!checked[r][r].isEmpty()){
				Piece pos = checked[r][r].peek();
				if(pos.getId() == myID){
					score += 3;
					if(pos.getSize() == 4){
						score += 1;
					}
				} else if(pos.getId() != myID){
					score += -1;
				}
			}
			if(!checked[r][3-r].isEmpty()){
				Piece pos2 = checked[r][3-r].peek();
				if(pos2.getId() == myID){
					score += 3;
					if(pos2.getSize() == 4){
						score += 1;
					}
				} else if(pos2.getId() != myID){
					score += -1;
				}
			}
		}
		return score;
	}
	/**
	 * checks for winning and losing moves and plans according to them. will later go more in depth
	 * for better strategy
	 * 
	 * @param move - a legal playermove strategy
	 * @return the "best" move
	 */
	private int moveInt(PlayerMove move){
		int total = 0;
		int lines3 = 0;
		Stack<Piece>[][] board2 = null;
		Stack<Piece>[] myStacks2 = null;
		Stack<Piece>[] oppStacks2 = null;
		Stack<Piece>[][] board3 = null;
		Stack<Piece>[] myStacks3 = null;
		Stack<Piece>[] oppStacks3 = null;
		board2 = (Stack<Piece>[][]) Cloner.deepCopy(board);
		myStacks2 = (Stack<Piece>[])Cloner.deepCopy(myStacks);
		oppStacks2 = (Stack<Piece>[])Cloner.deepCopy(oppStacks);
		if(move.getStack() == 0){
			int row = move.getStartRow();
			int col = move.getStartCol();
			Piece moved = board2[row][col].pop();
			int row2 = move.getEndRow();
			int col2 = move.getEndCol();
			board2[row2][col2].push(moved);
		} else {
			int stackNum = (move.getStack() - 1);
			if(move.getPlayerId() == myID){
				Piece moved = myStacks2[stackNum].pop();
				int row = move.getEndRow();
				int col = move.getEndCol();
				board2[row][col].push(moved);
			} else {
				Piece moved = oppStacks2[stackNum].pop();
				int row = move.getEndRow();
				int col = move.getEndCol();
				board2[row][col].push(moved);
			}
		}
		total = threeLines(board2);
		int winline = 0;
		for(int r = 0; r < 4; r++){
			winline = 0;
			for(int c = 0; c < 4; c++){
				if(!board2[r][c].isEmpty()){
					if(board2[r][c].peek().getId() != myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return -1000;
			}
		}
		for(int c2 = 0; c2 < 4; c2++){
			winline = 0;
			for(int r2 = 0; r2 < 4; r2++){
				if(!board2[r2][c2].isEmpty()){
					if(board2[r2][c2].peek().getId() != myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return -1000;
			}
		}
		winline = 0;
		for(int rc = 0; rc < 4; rc ++){
			if(!board2[rc][rc].isEmpty()){
				if(board2[rc][rc].peek().getId() != myID){
					winline += 1;
				}
			}
		}
		if(winline == 4){
			return -1000;
		}
		winline = 0;
		for(int rc = 0; rc < 4; rc ++){
			if(!board2[rc][3-rc].isEmpty()){
				if(board2[rc][3-rc].peek().getId() != myID){
					winline += 1;
				}
			}
		}
		if(winline == 4){
			return -1000;
		}
		winline = 0;
		for(int r = 0; r < 4; r++){
			winline = 0;
			for(int c = 0; c < 4; c++){
				if(!board2[r][c].isEmpty()){
					if(board2[r][c].peek().getId() == myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return 1000;
			}else if(winline == 2){
				total += 3;
			}else if(winline == 3){
				total += 4;
				lines3 += 1;
			}
		}
		for(int c2 = 0; c2 < 4; c2++){
			winline = 0;
			for(int r2 = 0; r2 < 4; r2++){
				if(!board2[r2][c2].isEmpty()){
					if(board2[r2][c2].peek().getId() == myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return 1000;
			}else if(winline == 2){
				total += 3;
			}else if(winline == 3){
				total += 4;
				lines3 += 1;
			}
		}
		winline = 0;
		for(int rc = 0; rc < 4; rc ++){
			if(!board2[rc][rc].isEmpty()){
				if(board2[rc][rc].peek().getId() == myID){
					winline += 1;
				}
			}
		}
		if(winline == 4){
			return 1000;
		}else if(winline == 2){
			total += 3;
		}else if(winline == 3){
			total += 8;
			lines3 += 1;
		}
		winline = 0;
		for(int rc = 0; rc < 4; rc ++){
			if(!board2[rc][3-rc].isEmpty()){
				if(board2[rc][3-rc].peek().getId() == myID){
					winline += 1;
				}
			}
		}
		if(winline == 4){
			return 1000;
		}else if(winline == 2){
			total += 3;
		}else if(winline == 3){
			total += 8;
			lines3 += 1;
		}
		
		//check for 4 in a row here of my pieces after checking for 4 in a row of his pieces
		//Return this move as instant win if it wins, instant lose if he won.
		List<PlayerMove> legalMoves = null;
		if(myID == 1){
			legalMoves = generateMoves(2, board2);
		} else {
			legalMoves = generateMoves(1, board2);
		}
		for(PlayerMove oppmove : legalMoves){
			board3 = (Stack<Piece>[][])Cloner.deepCopy(board2);
			myStacks3 = (Stack<Piece>[])Cloner.deepCopy(myStacks2);
			oppStacks3 = (Stack<Piece>[])Cloner.deepCopy(oppStacks2);
			if(oppmove.getStack() == 0){
				int row = oppmove.getStartRow();
				int col = oppmove.getStartCol();
				Piece moved = board3[row][col].pop();
				int row2 = oppmove.getEndRow();
				int col2 = oppmove.getEndCol();
				board3[row2][col2].push(moved);
			} else {
				int stackNum = (oppmove.getStack() - 1);
				if(oppmove.getPlayerId() == myID){
					Piece moved = myStacks3[stackNum].pop();
					int row = oppmove.getEndRow();
					int col = oppmove.getEndCol();
					board3[row][col].push(moved);
				} else {
					Piece moved = oppStacks3[stackNum].pop();
					int row = oppmove.getEndRow();
					int col = oppmove.getEndCol();
					board3[row][col].push(moved);
				}
			}
			for(int r = 0; r < 4; r++){
				winline = 0;
				for(int c = 0; c < 4; c++){
					if(!board3[r][c].isEmpty()){
						if(board3[r][c].peek().getId() != myID){
							winline += 1;
						}
					}
				}
				if(winline == 4){
					return -1000;
				}
			}
			for(int c2 = 0; c2 < 4; c2++){
				winline = 0;
				for(int r2 = 0; r2 < 4; r2++){
					if(!board3[r2][c2].isEmpty()){
						if(board3[r2][c2].peek().getId() != myID){
							winline += 1;
						}
					}
				}
				if(winline == 4){
					return -1000;
				}
			}
			winline = 0;
			for(int rc = 0; rc < 4; rc ++){
				if(!board3[rc][rc].isEmpty()){
					if(board3[rc][rc].peek().getId() != myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return -1000;
			}
			winline = 0;
			for(int rc = 0; rc < 4; rc ++){
				if(!board3[rc][3-rc].isEmpty()){
					if(board3[rc][3-rc].peek().getId() != myID){
						winline += 1;
					}
				}
			}
			if(winline == 4){
				return -1000;
			}
			//start making decisions about this move mostly just checking for th opponent winning.
			//other decisions about this will be made later
		}

		if(lines3 >1){
			total += 500;
		}
		return total;
	}
	/**
	 * checks the integer values of moves against each other to find the best move
	 * 
	 * @param legalMoves - the list of legal moves
	 * @return the "best" move
	 */
	private PlayerMove strategy(List<PlayerMove> legalMoves){
		int max = -20000;
		List<PlayerMove> bestMoves = new ArrayList<PlayerMove>();
		PlayerMove bestmove = null;
		for(PlayerMove move: legalMoves){
			int cur = moveInt(move);
			if(cur > max){
				bestMoves = new ArrayList<PlayerMove>();
				max = cur;
				bestMoves.add(move);
			} else if(cur == max){
				bestMoves.add(move);
			}
		}
		Collections.shuffle(bestMoves);
		bestmove = bestMoves.get(0);
		
		return bestmove;
	}
	

	/*
	 * not to be done
	 */
	@Override
	public void playerInvalidated(int arg0) {
		// done

	}

}
