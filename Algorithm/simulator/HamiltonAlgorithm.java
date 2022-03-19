package simulator;
// Java Program to Solve Travelling Salesman Problem
// Using Incremental Insertion Method
 
// Importing input output classes
import java.io.*;
// Importing Scanner class to take input from the user
import java.util.Scanner;
import java.util.ArrayList;

import java.lang.Math;
 
// Main class
public class HamiltonAlgorithm {
    // Travelling Salesman Incremental Insertion Method
    static int tspdp(int c[][], int tour[], int start,
                     int n) //n = final index
    {
 
        int mintour[] = new int[n+1], temp[] = new int[n+1],
            mincost = 999, ccost, i, j, k;
 
        if (start == n - 1) 
        {
            return c[tour[n - 1]][tour[n]];
                   // + c[tour[n]][1]); 
        }
 
        // Logic for implementing the minimal cost
 
        for (i = start + 1; i <= n; i++)
        {
            for (j = 1; j <= n; j++)
                temp[j] = tour[j];
            temp[start + 1] = tour[i];
            temp[i] = tour[start + 1];
         //compare the cost of travelling to each node from start node and identify the cheapest
		 //recursively call subgraph from start+1 to n to identify optimal path for subgraph
            if ((c[tour[start]][tour[i]] + (ccost = tspdp(c, temp, start + 1, n)))< mincost) 
            {
                mincost = c[tour[start]][tour[i]] + ccost;
                for (k = 0; k <= n; k++)
                    mintour[k] = temp[k];
            }
        }
 
        // Now, iterating over the path (mintour) to
        // compute its cost
        for (i = 0; i <= n; i++)
            tour[i] = mintour[i];
 
        // Returning the cost of min path
        return mincost;
    }
	
	public  static int[][] generateGraphMatrix(int nodes[][], int n){
		int mat[][] = new int[n][n];
		int dist = 0;
		for(int i=0;i<n;i++)
			mat[i][i] = 0;//dist is 0 to self
		for(int i=0;i<n-1;i++){
			for(int j=i;j<n;j++){
				dist = calcDistance(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1]);
				mat[i][j] = dist;
				mat[j][i] = dist;
			}
		}
		return mat;
	}
	
	public static int calcDistance(int x1, int y1, int x2, int y2){
		return (int)(Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))+0.5); //rounds off to nearest int
	}
 
	public static void printMat(int[][] mat, int n){
		for(int i =0; i<n; i++){
			for(int j=0;j<n;j++){
				System.out.print(mat[i][j]+" ");
			}
			System.out.println();
		}
	}
	
	public static int findPathDistance(int graphMat[][], int path[], int n){
		int dist=0;
		for(int i = 0; i<n; i++){
			dist+=graphMat[path[i]][path[i+1]];
		}
		return dist;
	}
	
	public static int[] reversePath(int path[], int n){
		int rPath[]=new int[n+1];
		rPath[0] = 0;
		for(int i = 1;i<=n;i++){
			rPath[i] = path[n-i+1]; 
		}
		return rPath;
	}
	
	//Key function to find hamiltonian path called by Map
	public static int[] findOptimalPath(ArrayList<ImageBlock> imgBlocks, Car car){
		int n = imgBlocks.size();
		int nodes[][] = new int[n+1][2];
		int cost;
		nodes[0] = car.getPos();
		for(int i = 1;i<n+1;i++){
			nodes[i] = imgBlocks.get(i-1).getPos().clone();
			switch(imgBlocks.get(i-1).getDir()) {
				case 'N':
					nodes[i][1] -= 3;
					break;
				case 'E':
					nodes[i][0] += 3;
					break;
				case 'S':
					nodes[i][1] += 3;
					break;
				case 'W':
					nodes[i][0] -= 3;
					break;
			}
		}
		int graphMat[][] = generateGraphMatrix(nodes, n+1); //+1 to include start pos
		int tour[] = new int[n+1];
		for (int i = 0; i <= n; i++)
			tour[i] = i; //initialize path
		
		//find optimal tsp cost and path
		cost = tspdp(graphMat, tour, 0, n);
		
		int rPath[] = reversePath(tour,n); //reverse path to check if the reverse of the path is more optimal
		int rPathDist = findPathDistance(graphMat,rPath,n);
		System.out.print("\n**Optimal path = ");
        if(cost<rPathDist){ 
			for (int i = 0; i <= n; i++){
	 
				// Printing across which cities should Salesman
				// travel
				if(i<n)
					System.out.print(tour[i] + "->");
				else
					System.out.print(tour[i]);
				
			}
			// Print and display the (minimum)cost of the path
			// traversed
			System.out.println("/nMinimum Cost: " + cost);
			return tour;
		}else{

			for (int i = 0; i <= n; i++){

			// Printing across which cities should Salesman
			// travel
			if(i<n)
				System.out.print(rPath[i] + "->");
			else
				System.out.print(rPath[i]);
			}
			// Print and display the (minimum)cost of the reversed path
			// traversed
			System.out.println("/nMinimum Cost: " + rPathDist);
			return rPath;
		}
	}


}