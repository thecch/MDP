package simulator;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;

public class Node{
	private float g,h,f;
	private int type;//type 0=available node,1=obstacle
	private int[] pos = new int[2];
	private Node parent;

	public Node(int x, int y){
		this.pos[0] = x;
		this.pos[1] = y;
		this.g=0;
		this.h=0;
		this.f=0;
		this.type = 0;
	}
	
	
	public void setObstacle(){ type = 1;}
	
	public void remObstacle(){ type = 0;}
	
	public int getType(){ return type; }
	
	public int[] getPos(){
		return pos;
	}
	
	public void setVal(float g, float h){
		this.g = g;
		this.h = h;
		this.f = g+h;
	}
	
	public float getG(){ return g;}
	public float getH(){ return h;}
	public float getF(){ return f;}
	
	public void setParent(Node p){parent = p;}
	public Node getParent(){return parent;}
	
	public void printNode(){
		System.out.println("Node pos: " + Arrays.toString(pos)+"\nG = "+g+"\nH = "+h+"\nF = "+f);
	}
	
}