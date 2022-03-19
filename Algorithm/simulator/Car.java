package simulator;

import java.awt.*;
import java.util.ArrayList;

public class Car{
	private int[] pos;
	private int facing;
	private int size; //car size will be size*size grid 
	public Car(int x,int y, int facing, int size){
		pos = new int[2];
		pos[0] = x;
		pos[1] = y;
		this.facing = facing;
		this.size = size;
	}
	public int[] getPos(){
		return pos;
	}
	
	public int getFacing(){
		return facing;
	}
	
	public int getSize(){
		return size;
	}
	
	//move forward and backwards: +ve = forward, -ve = backwards
	public void moveFB(int steps){
		switch(facing){
			//0-North, 2-East, 4-South, 6-West
			case 0:
				pos[1] -= steps;
				break;
			case 1:
				pos[0] += steps;
				pos[1] -= steps;
				break;
			case 2:
				pos[0] += steps;
				break;
			case 3:
				pos[0] += steps;
				pos[1] += steps;
				break;
			case 4:
				pos[1] += steps;
				break;
			case 5:
				pos[0] -= steps;
				pos[1] += steps;
				break;
			case 6:
				pos[0] -= steps;
				break;
			case 7:
				pos[0] -= steps;
				pos[1] -= steps;
				break;
			default:
				break;
		}
	}

	public void turn(int direction){
		//+ve clockwise, -ve anti-clockwise
		facing = (facing+direction)%8;
		if(facing<0)
			facing = 8 + facing;
	}
	
	
}