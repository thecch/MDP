package simulator;

import java.awt.*;
import java.util.ArrayList;

public class ImageBlock{
	private int[] pos;
	private char dir;
	private int index;  //its index in the imgBlocks list in Map
	public ImageBlock(int x, int y, char dir,int index){
		pos = new int[2];
		pos[0] = x;
		pos[1] = y;
		this.dir = dir;
		this.index = index;
	}
	
	public int[] getPos(){
		return pos;
	}
	public char getDir(){
		return dir;
	}
	public int getIndex(){
		return index;
	}
}