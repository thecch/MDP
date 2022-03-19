package simulator;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;


public class Map{
	private int size = 20;
	private int iteration = 0;
	private char[][] grid;
	private Node[][] nodeGrid;
	private ArrayList<ImageBlock> imgBlocks;
	//binary list to check if imgs are cleared
	private int clearList[];
	private int clearCount;
	private Car car;
	//init map with start pos of car
	public Map(int startPosX,int startPosY,int facing){
		grid = new char[size][size];
		car = new Car(startPosX,startPosY,facing,3);
		imgBlocks = new ArrayList<ImageBlock>();
		clearCount = 0;
		nodeGrid = new Node[size][size];
		initMap();
	}
	
	//init values of each map grid and car direction
	public void initMap(){
		for(int i = 0;i<size;i++){
			for(int j=0;j<size;j++){
				grid[i][j] = '-';
				nodeGrid[i][j] = new Node(i,j);
			}
		}
		drawCar();
	}
	/*x,y = coordinate on grid
	  dir = 'N', 'S', 'E' , 'W'
	*/
	public void addBlock(int x, int y, char dir){
		ImageBlock ib = new ImageBlock(x,y,dir,imgBlocks.size()+1);
		imgBlocks.add(ib);
		grid[x][y] = dir;
		for(int i=x-1; i<=x+1; i++) {
			for(int j=y-1; j<=y+1; j++) {
				if(i>=0 && i<=19 && j>=0 && j<=19) 
					nodeGrid[i][j].setObstacle();
			}
		}
	}
	
	public int[] findPath(){
		//initialize clear list since obstacles are fixed at this point
		clearList = new int[imgBlocks.size()];
		for (int i=0;i<imgBlocks.size();i++)
			clearList[i]=0;
		return HamiltonAlgorithm.findOptimalPath(imgBlocks,car);
	}
	
	public void completeImage(int img){
		clearList[img] = 1;
		clearCount++;
	}
	
	public int getClearCount(){
		return clearCount;
	}
	
	public int getIteration() {
		return iteration;
	}
	
	public void printMap(){
		System.out.println("\n======ITERATION "+iteration+" Images cleared: "+clearCount+"======");
		System.out.print("  ");
		for(int i = 0;i<size;i++)
			System.out.print(i%10 + " ");
		System.out.println();
		for(int i = 0;i<size;i++){
			System.out.print(i%10 + " ");
			for(int j=0;j<size;j++){
				System.out.print(grid[j][i]+" ");
			}
			System.out.println();
		}
		iteration++;
	}
	
	public int moveToTarget(int target) {
		int[] tarPos = calibTarget(target);	//receive target location of car
		int[] nextDif = new int[2];			//init difference of between target and car
		int i = 0;							//init integer to iterate through path
		int j;								//init loop integer
		int face = 0;						//init car face
		int diff = 0;
		Node cur;
		ImageBlock tarBlock = imgBlocks.get(target);
		
		//Get PTPPath
		insertMoveOffObs();
		ArrayList<Node> path = Astar.findPath(nodeGrid, car.getPos(), tarPos);
		deleteMoveOffObs();
		
		if(tarPos[0] != getTarget(target)[0] || tarPos[1] != getTarget(target)[1]) {
			insertMoveOffObs(tarPos, tarBlock.getDir());
			path.addAll(Astar.findPath(nodeGrid, tarPos, getTarget(target)));
			deleteMoveOffObs(tarPos, tarBlock.getDir());
		}
		
		for(j = 0;j<path.size();j++){
			grid[path.get(j).getPos()[0]][path.get(j).getPos()[1]] = '+';
		}
		
		
		while(i<path.size()) {
			nextDif = path.get(i).getPos().clone();
			if(Arrays.equals(nextDif, car.getPos())) i++;
			else {
				nextDif[0] -= car.getPos()[0];
				nextDif[1] -= car.getPos()[1];
				
				if(moveCarXY(nextDif)==1)
					i++;
				//resetImgs();
				printMap();
			}
		}
		
		//Reached in front of obstacle
		if(tarBlock.getDir() == 'N') 
			face = 4;
		else if(tarBlock.getDir() == 'E') 
			face = 6;
		else if(tarBlock.getDir() == 'S')
			face = 0;
		else if(tarBlock.getDir() == 'W')
			face = 2;
		
		//Get the car to face correct direction (Turns on the spot)
		while(car.getFacing() != face){
			diff = face - car.getFacing();
			if(diff < 0)
				diff += 8;

			if(diff > 4)
				turnCar(-1);
			else
				turnCar(1);
			printMap();
		}
		
		//Complete image
		completeImage(target);
		
		return 1;
	
	}
	
	/*temp function to place obstacles back at original spot*/
	private void resetImgs(){
		for(int i=0;i<imgBlocks.size();i++){
			int imgPos[] = imgBlocks.get(i).getPos();
			if(grid[imgPos[0]][imgPos[1]]=='-')
				grid[imgPos[0]][imgPos[1]]=imgBlocks.get(i).getDir();
		}
	}
	//car functions
	private int moveCarXY(int[] pos) {
		int face=0;
		
		//Get car target direction
		if(pos[0] == 0 && pos[1] < 0)
			face = 0;
		else if(pos[0] > 0 && pos[1] < 0)
			face = 1;
		else if(pos[0] > 0 && pos[1] == 0)
			face = 2;
		else if(pos[0] > 0 && pos[1] > 0)
			face = 3;
		else if(pos[0] == 0 && pos[1] > 0)
			face = 4;
		else if(pos[0] < 0 && pos[1] > 0)
			face = 5;
		else if(pos[0] < 0 && pos[1] == 0)
			face = 6;
		else if(pos[0] < 0 && pos[1] < 0)
			face = 7;
		
		
		if(car.getFacing() == face) {
			//Move car if facing right direction
			moveCarFB(1);
			return 1;
		}else {
			//Turn car if facing incorrect direction with minimum turning range
			if(face-car.getFacing() < 0)
				face += 8;

			if(face-car.getFacing() > 4)
				turnCar(-1);
			else
				turnCar(1);
		}
		
		return 0;
	}
	
	private void moveCarFB(int steps){
		//grid[car.getPos()[0]][car.getPos()[1]] = '-';
		eraseCar();
		car.moveFB(steps);
		//grid[car.getPos()[0]][car.getPos()[1]] = getCar();
		drawCar();
		System.out.println("Moving car forward by "+steps+" steps");
	}
	
	private void turnCar(int direction){
		//eraseCar();
		car.turn(direction);
		//grid[car.getPos()[0]][car.getPos()[1]] = getCar();
		drawCar();
		System.out.println("Turning car towards "+direction);
	}
	
	private int[] getCarFace() {
		int pos[] = car.getPos().clone();;
		switch(car.getFacing()){
			case 0:
				pos[1] -= 1;
				break;
			case 1:
				pos[0] += 1;
				pos[1] -= 1;
				break;
			case 2:
				pos[0] += 1;
				break;
			case 3:
				pos[0] += 1;
				pos[1] += 1;
				break;
			case 4:
				pos[1] += 1;
				break;
			case 5:
				pos[0] -= 1;
				pos[1] += 1;
				break;
			case 6:
				pos[0] -= 1;
				break;
			case 7:
				pos[0] -= 1;
				pos[1] -= 1;
				break;
			default:
				break;
		}
		
		return pos;
	}
	//erase car on map
	private void eraseCar(){
		int pos[] = car.getPos();
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						grid[pos[0]+i][pos[1]+j] = '-';
			}
		}
	}
	//draw car on map
	private void drawCar(){
		int pos[] = car.getPos();
		int face[] = getCarFace();
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						if(i==0&&j==0)
							grid[pos[0]][pos[1]] = '@'; //Draw center of car
						else if((pos[0]+i)==face[0]&&(pos[1]+j)==face[1])
							grid[face[0]][face[1]] = '*'; //Draw face of car
						else
							grid[pos[0]+i][pos[1]+j] = '#';
			}
		}
	}
	
	
	
	//get supposed stopping position of car
	private int[] getTarget(int target) {
		int[] tarPos;
		
		ImageBlock tarBlock = imgBlocks.get(target);
		tarPos = tarBlock.getPos().clone();
		
		switch(tarBlock.getDir()) {
			case 'N':
				tarPos[1] -= 3;
				break;
			case 'E':
				tarPos[0] += 3;
				break;
			case 'S':
				tarPos[1] += 3;
				break;
			case 'W':
				tarPos[0] -= 3;
				break;
		}
		
		return tarPos;
	}
	
	//get position of car before moving to target for adjustment
	private int[] calibTarget(int target) {
		int[] calibPos, posDif;
		
		ImageBlock tarBlock = imgBlocks.get(target);
		calibPos = tarBlock.getPos().clone();
		posDif = tarBlock.getPos().clone();
		posDif[0] -= car.getPos()[0];
		posDif[1] -= car.getPos()[1];
		
		switch(tarBlock.getDir()) {
			case 'N':
				calibPos[1] -= 3;
				if(posDif[1] <= 0) {
					if(posDif[0] > 0 && calibPos[0]-3 >= 0)
						calibPos[0] -= 3;
					else
						calibPos[0] += 3;
				}
				break;
			case 'S':
				calibPos[1] += 3;
				if(posDif[1] >= 0) {
					if(posDif[0] > 0 && calibPos[0]-3 >= 0)
						calibPos[0] -= 3;
					else
						calibPos[0] += 3;
				}
				break;
			case 'E':
				calibPos[0] += 3;
				if(posDif[0] >= 0) {
					if(posDif[1] > 0 && calibPos[1]-3 >= 0)
						calibPos[1] -= 3;
					else
						calibPos[1] += 3;
				}
				break;
			case 'W':
				calibPos[0] -= 3;
				if(posDif[0] <= 0) {
					if(posDif[1] > 0 && calibPos[1]-3 >= 0)
						calibPos[1] -= 3;
					else
						calibPos[1] += 3;
				}
				break;
		}
		
		return calibPos;
	}
	
	//Insert obstacle for moving off from target
	private void insertMoveOffObs() {
		int pos[] = car.getPos();
		int faceDif[] = getCarFace().clone();
		faceDif[0] -= pos[0];
		faceDif[1] -= pos[1];
		
		System.out.println("Difference: (" + faceDif[0] + "," + faceDif[1] + ")");
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						if((i==0&&j==0)||(i==faceDif[0]&&j==0)||(i==0&&j==faceDif[1])) //avoid face and centre of car
							continue;
						else if(faceDif[0]==0&&j==faceDif[1]&&(i==faceDif[0]+1||i==faceDif[0]-1)) //avoid side of face of car
							continue;
						else if(faceDif[1]==0&&i==faceDif[0]&&(j==faceDif[1]+1||j==faceDif[1]-1)) //avoid side of face of car
							continue;
						else
							nodeGrid[pos[0]+i][pos[1]+j].setObstacle(); //insert obstacle
			}
		}
	}
	
	//Remove obstacle for moving off from target
	private void deleteMoveOffObs() {
		int pos[] = car.getPos();
		int faceDif[] = getCarFace().clone();
		faceDif[0] -= pos[0];
		faceDif[1] -= pos[1];
		
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						if((i==0&&j==0)||(i==faceDif[0]&&j==0)||(i==0&&j==faceDif[1])) //avoid face and centre of car
							continue;
						else if(faceDif[0]==0&&j==faceDif[1]&&(i==faceDif[0]+1||i==faceDif[0]-1)) //avoid side of face of car
							continue;
						else if(faceDif[1]==0&&i==faceDif[0]&&(j==faceDif[1]+1||j==faceDif[1]-1)) //avoid side of face of car
							continue;
						else
							nodeGrid[pos[0]+i][pos[1]+j].remObstacle(); //insert obstacle
			}
		}
	}
	
	
	//Insert obstacle for reaching target
	private void insertMoveOffObs(int[] pos, char tarFace) {
		int faceDif[] = {0,0};
		
		//get initial face of car
		switch(tarFace) {
			case 'N':
				faceDif[0] = 0;
				faceDif[1] = -1;
				break;
			case 'S':
				faceDif[0] = 0;
				faceDif[1] = 1;
				break;
			case 'E':
				faceDif[0] = 1;
				faceDif[1] = 0;
				break;
			case 'W':
				faceDif[0] = -1;
				faceDif[1] = 0;
				break;
		}
		
		System.out.println("Difference: (" + faceDif[0] + "," + faceDif[1] + ")");
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						if((i==0&&j==0)||(i==faceDif[0]&&j==0)||(i==0&&j==faceDif[1])) //avoid face and centre of car
							continue;
						else if(faceDif[0]==0&&j==faceDif[1]&&(i==faceDif[0]+1||i==faceDif[0]-1)) //avoid side of face of car
							continue;
						else if(faceDif[1]==0&&i==faceDif[0]&&(j==faceDif[1]+1||j==faceDif[1]-1)) //avoid side of face of car
							continue;
						else
							nodeGrid[pos[0]+i][pos[1]+j].setObstacle(); //insert obstacle
			}
		}
	}
	
	//Delete obstacle for reaching target
	private void deleteMoveOffObs(int[] pos, char tarFace) {
		int faceDif[] = {0,0};
		
		//get initial face of car
		switch(tarFace) {
			case 'N':
				faceDif[0] = 0;
				faceDif[1] = -1;
				break;
			case 'S':
				faceDif[0] = 0;
				faceDif[1] = 1;
				break;
			case 'E':
				faceDif[0] = 1;
				faceDif[1] = 0;
				break;
			case 'W':
				faceDif[0] = -1;
				faceDif[1] = 0;
				break;
		}
		
		int extrusion = (car.getSize()-1)/2; //how much to extrude from centre of car
		for(int i = -extrusion;i<=extrusion;i++){
			for(int j = -extrusion;j<=extrusion;j++){
				if(pos[0]+i>=0&&pos[1]+j>=0) //no negative index
					if(pos[0]+i<=size-1&&pos[1]+j<=size-1) //no index beyond map size
						if((i==0&&j==0)||(i==faceDif[0]&&j==0)||(i==0&&j==faceDif[1])) //avoid face and centre of car
							continue;
						else if(faceDif[0]==0&&j==faceDif[1]&&(i==faceDif[0]+1||i==faceDif[0]-1)) //avoid side of face of car
							continue;
						else if(faceDif[1]==0&&i==faceDif[0]&&(j==faceDif[1]+1||j==faceDif[1]-1)) //avoid side of face of car
							continue;
						else
							nodeGrid[pos[0]+i][pos[1]+j].remObstacle(); //insert obstacle
			}
		}
	}
	
	//for debug purposes
	public void getPTPPath(int[] destPos){
		int startPos[] = car.getPos();
		//int destPos[] = imgBlocks.get(0).getPos();
		ArrayList<Node> path = Astar.findPath(nodeGrid, startPos, destPos);
		for(int i = 0;i<path.size();i++){
			System.out.println(Arrays.toString(path.get(i).getPos()));
			grid[path.get(i).getPos()[0]][path.get(i).getPos()[1]] = '+';
		}
		printMap();
		//return path;
	}
}





