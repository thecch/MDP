package simulator;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;

public class Main{
	public static Map m;
	public static int path[];
	public static ArrayList<Integer> pathLeft;
	public Main(){}
	public static void main(String args[]){
		pathLeft = new ArrayList<Integer>();
		
		m = new Map(1,18,0);
		m.addBlock(4,5,'N');
		m.addBlock(9,9,'E');
		m.addBlock(10,5,'W');
		m.addBlock(19,16,'W');
		m.addBlock(18,0,'S');
		
		path=m.findPath();
		
		for (int j=1; j<path.length; j++) {
			pathLeft.add(path[j]);
		}
		
		System.out.println(pathLeft);
		
		int destPos[] = {16,16}; // destPos
		//m.getPTPPath(destPos); //uncomment this to show Astar path
		m.printMap();
		
		while(!(pathLeft.isEmpty())) {
			System.out.println("Current Target: "+path[m.getClearCount()+1]);
			if(m.moveToTarget(pathLeft.get(0)-1)==1)
				pathLeft.remove(0);
		}
		
		m.printMap();
		
	}
	

}