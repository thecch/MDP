package simulator;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.lang.Math;
public class Astar{
	private static int size;
	
	public static ArrayList<Node> findPath(Node[][] map, int[] startPos, int[] destPos){
		Node start = map[startPos[0]][startPos[1]];
		Node dest = map[destPos[0]][destPos[1]];
		ArrayList<Node> open = new ArrayList<Node>();
		ArrayList<Node> closed = new ArrayList<Node>();
		Node cur;
		size = map.length;
		open.add(start);
		//start.printNode();
		do{
			//int pos[] = getCheapestNode(open).getPos();
			cur = getCheapestNode(open); //open is somehow empty
			//cur.getPos();
			open.remove(cur);
			closed.add(cur);
			if(cur == dest){
				return retracePath(start , dest);
			}
			ArrayList<Node> pList = getNeighbour(map, cur, dest);
			//System.out.println(pList.size());
			for(int i = 0;i<pList.size();i++){
				Node n = pList.get(i);
				if(n.getType() != 1 &&!closed.contains(n)){
					float distToN = cur.getG() + calcDistance(cur,n); //new distance from start to neighbour
					if(!open.contains(n)||distToN<n.getG()){
						initNode(n, cur, dest);
						//n.printNode();
						if(!open.contains(n))
							open.add(n);
					}
						
				}
			}
			
		}while(open.size()>0);
		return closed; //temp
	}
	
	public static ArrayList<Node> retracePath(Node start, Node dest){
		ArrayList<Node> path = new ArrayList<Node>();
		Node cur = dest;
		path.add(cur);
		while(cur!=start){
			cur = cur.getParent();
			path.add(0,cur); // add node to front
		}
		return path;
	}
	public static Node getCheapestNode(ArrayList<Node> nl){
		float min = 9999;
		int cheapest=0;
		if(nl.size()>0){
			//System.out.println(nl.size());
			for(int i=0;i<nl.size();i++){
				if(nl.get(i).getF()<min){
					//System.out.println(nl.get(i).getF());
					min = nl.get(i).getF();
					cheapest = i;
				}
			}
			return nl.get(cheapest);
		}
		else{ 
			System.out.println("empty");
			return null;
		}
	}
	
	public static void initNode(Node targetNode, Node parent, Node dest){
		targetNode.setParent(parent);
		float g,h;		
		if(targetNode.getH() == 0)
			h = calcDistance(targetNode, dest);
		else
			h = targetNode.getH();
		g = parent.getG()+ calcDistance(targetNode, parent);
		targetNode.setVal(g,h);
		//targetNode.printNode();
	}
	
	
	public static float calcDistance(Node from, Node to){
		int x1 = from.getPos()[0];
		int y1 = from.getPos()[1];
		int x2 = to.getPos()[0];
		int y2 = to.getPos()[1];
		return ((float)Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))); //rounds off to nearest int
	}
	
	public static ArrayList<Node> getNeighbour(Node[][] map, Node n, Node dest){
		ArrayList<Node> pList = new ArrayList<Node>();
		//System.out.println(Arrays.toString(n.getPos()));
		int pos[] = n.getPos();
		for(int i = -1; i<=1;i++){
			for(int j = -1;j<=1;j++){
				if(pos[0]+i<0||pos[1]+j<0){}
				else if(pos[0]+i>=size||pos[1]+j>=size){ }
				else if(i==0&&j==0){}
				else{//no index beyond map size
						//if(i!=0&&j!=0){
							//map[pos[0]+i][pos[1]+j].printNode();
							pList.add(map[pos[0]+i][pos[1]+j]);
						//}
				}
			}
		}
		return pList;
	}
}