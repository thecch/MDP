public class Vehicle {
	private int x;
	private int y;
	private int width;
	private int length;
	private double angle;
	
	public Vehicle(int x, int y, int width, int length, double angle) {
		this.x = x;
		this.y = y;
		this.width = width;
		this.length = length;
		this.angle = angle;
	}
	
	public int getX(){
		return x;
	}
	
	public void setX(int x){
		this.x = x;
	}
	
	public int getY(){
		return y;
	}
	
	public void setY(int y){
		this.y = y;
	}
	
	public int getWidth(){
		return width;
	}
	
	public void setWidth(int width){
		this.width = width;
	}
	
	public int getLength(){
		return length;
	}
	
	public void setLength(int length){
		this.length = length;
	}
	
	public double getAngle(){
		return angle;
	}
	
	public void setAngle(double angle){
		this.angle = angle;
	}
	
	
}
