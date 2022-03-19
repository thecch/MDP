import java.awt.*;
import javax.swing.*;
import java.util.ArrayList;

public class Grid {
	
	private Image carImage;

    public static void main(String[] args) {
        new Grid();
    }

    public Grid() {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException ex) {
                    ex.printStackTrace();
                }

                JFrame frame = new JFrame("Testing");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.add(new TestPane());
                frame.pack();
                frame.setLocationRelativeTo(null);
                frame.setVisible(true);
            }
        });
    }

    public class TestPane extends JPanel {

		int size;
		int width;
		int height;
		ArrayList<Obstacle> obstacleList = new ArrayList<>();
		Vehicle car;
		
		
        public TestPane() {
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(400, 400); //JPanel window dimension
        }

        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g.create();
            size = Math.min(getWidth() - 4, getHeight() - 4)/20; //size of each rectangle to be the smaller of the height or width - margin offset, /20 for 20 rectangles vertically and horizontally
            width = getWidth() - (size * 2); //width of grid
            height = getHeight() - (size * 2); //height of grid
			//System.out.println("getWidth() = "+getWidth() + "\ngetHeight() = " + getHeight()); //JPanel's height and width
            int y = (getHeight() - (size * 20)) / 2; //initialize first rectangle y coordinate via panel size - (size of 20 rectangles). /2 for some offset(?)
            for (int horz = 0; horz < 20; horz++) { //loop for drwing 20 rectangles
                int x = (getWidth() - (size * 20)) / 2; ///initialize first rectangle x coordinate via panel size - (size of 20 rectangles). /2 for some offset(?)
                for (int vert = 0; vert < 20; vert++) {
                    g.drawRect(x, y, size, size);
					
                    x += size; // increment x by the size of each rectangle for the next rectangle
                }
                y += size;
            }
			createObstacle(5,5,ObsDir.NORTH,g);
			createObstacle(12,4,ObsDir.EAST,g);
			createObstacle(6,8,ObsDir.WEST,g);
			loadImages();
			initStartZone(g);
			initVehicle(g);
            g2d.dispose();
        }
		
		public void createObstacle(int x, int y, ObsDir dir, Graphics g){ //x = x coord to place obstacle //y = y coord to place obstacle //dir is direction the image is facing
			obstacleList.add(new Obstacle(x, y, dir));
			g.setColor(Color.RED);
			if (dir==ObsDir.EAST) g.setColor(Color.BLUE);
			else if (dir==ObsDir.SOUTH) g.setColor(Color.GREEN);
			else if (dir==ObsDir.WEST) g.setColor(Color.YELLOW);
			int ry = (getHeight() - (size * 20)) / 2;
			int rx = (getWidth() - (size * 20)) / 2;
			ry += size*y;
			rx += size*x;
			g.fillRect(rx,ry,size,size);
		}
		
		public void initStartZone(Graphics g) {
			g.setColor(Color.GRAY);
			int ry = (getHeight() - (size * 20)) / 2;
			int rx = (getWidth() - (size * 20)) / 2;
			for (int i=16; i < 20; i++) {
				for (int j=0; j < 4; j++) {
					g.fillRect(rx+size*j,ry+size*i,size,size);
				}
			}
		}
		
		public void loadImages() {
			ImageIcon carIcon = new ImageIcon("src/car.png");
			Image largeCar = carIcon.getImage();
			if (largeCar != null) {
				int width = (int)(size*3);
				int height = (int)(size*carIcon.getIconHeight()/carIcon.getIconWidth()*3);
				carIcon = new ImageIcon(largeCar.getScaledInstance(width, height, Image.SCALE_SMOOTH));
				carImage = carIcon.getImage();
			}
		}
		
		public void initVehicle(Graphics g) {
			int x = 1;
			int y = 18;
			car = new Vehicle(x, y, 3, 3, Math.PI/2);
			int ry = (getHeight() - (size *20)) / 2;
			int rx = (getWidth() - (size * 20)) / 2;
			ry += size*(y-1);
			rx += size*(x-1);
			g.drawImage(carImage, rx, ry, this);
		}
    }
}