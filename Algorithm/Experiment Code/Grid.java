import java.awt.*;
import javax.swing.*;
import java.lang.Math;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
public class Grid {

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
		Image car;
		ImageIcon carIcon;
		private int lastX = 0;
		private int lastY = 300;
		private double lastRot = 0;
        public TestPane() {
			Thread animationThread = new Thread(new Runnable() {
            public void run() {
                while (true) {
                    repaint();
                    try {Thread.sleep(10);} catch (Exception ex) {}
                }
				}
			});

			animationThread.start();
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
			placeObstacle(5,5,0,g);
			placeObstacle(12,4,1,g);
			placeObstacle(6,8,2,g);
			loadImages();
			initStartZone(g);
			initVehicle(g2d);
            //g2d.dispose();
        }
		
		public void placeObstacle(int x, int y, int dir, Graphics g){ //x = x coord to place obstacle //y = y coord to place obstacle //dir is direction the image is facing
			g.setColor(Color.RED);
			if (dir==1) g.setColor(Color.BLUE);
			else if (dir==2) g.setColor(Color.GREEN);
			else if (dir==3) g.setColor(Color.YELLOW);
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
			carIcon = new ImageIcon("src/car.png");
			Image largeCar = carIcon.getImage();
			if (largeCar != null) {
				int width = (int)(size*3);
				int height = (int)(size*carIcon.getIconHeight()/carIcon.getIconWidth()*3);
				carIcon = new ImageIcon(largeCar.getScaledInstance(width, height, Image.SCALE_SMOOTH));
				car = carIcon.getImage();
			}
		}
		
		public void initVehicle(Graphics2D g) {
			int ry = (getHeight() - (size *20)) / 2;
			int rx = (getWidth() - (size * 20)) / 2;

			ry += size*17;
			rx += size*0;
			
			int carW = (int)(size*3);
			int carH = (int)(size*carIcon.getIconHeight()/carIcon.getIconWidth()*3);
			int carSpeed = 1;
			int rotationSpeed = 1;
			double rotation = lastRot+Math.toRadians(rotationSpeed);
			
			//int x = lastX + carSpeed;
			int y = lastY - carSpeed;
			//AffineTransform tx = AffineTransform.getRotateInstance(rotation, rx, y);
			//AffineTransformOp op = new AffineTransformOp(tx, AffineTransformOp.TYPE_BILINEAR);
			g.rotate(rotation, rx+carW/2, ry+carH/2); //set pivot for rotation to be centre of the car
			g.drawImage(car, rx, ry, this);
			lastY = y;
			lastRot = rotation;
		}

    }
}
