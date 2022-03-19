public class Obstacle {
	private int x;
	private int y;
	private ObsDir dir;
	private int id;
	
	public Obstacle(int x, int y, ObsDir dir) {
		this.x = x;
		this.y = y;
		this.dir = dir;
		this.id = 0;
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
	
	public int getId(){
		return y;
	}
	
	public void setId(int id){
		this.id = id;
	}
	
	public ObsDir getDirection(){
		return dir;
	}
	
	public void setDirection(ObsDir dir){
		this.dir = dir;
	}
}
