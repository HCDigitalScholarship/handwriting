/*
  This program uses Processing. The main purpose of this program is to convert the SVG paths to X-Y coordinates. 
  Before running this program, you have to select Sketch option and Add a file to add the svg file into the Processing. 
  You can get the outputs from the console.
*/

PShape test; // declare a global PShape variable here.

void setup(){
  test = loadShape("testfile121.svg"); // set test to be the svg file through loadShape function.
  size(600, 600); // set the size of the window, which is not necessary.
  /*
    This nested for loop is to print out all the xy coordinates associated with each path in the SVG files.
  */
    for(int i = 0; i < test.getChildCount()-1; i++) // getChildCount() returns the number of paths in the SVG file.
  {
    PShape border = test.getChild(i); // get the path of the svg file.
    for(int j = 0 ; j < border.getVertexCount()-1; j++) {
      System.out.print(border.getVertexX(j) + ", ");
      //System.out.print("("+border.getVertexX(j) + ", " + border.getVertexY(j) + "), "); // print out all the xy-coordinates for the path.
    }
  }
  System.out.println();
  System.out.println();
  System.out.println();
  System.out.println();
    for(int i = 0; i < test.getChildCount()-1; i++) // getChildCount() returns the number of paths in the SVG file.
  {
    PShape border = test.getChild(i); // get the path of the svg file.
    for(int j = 0 ; j < border.getVertexCount()-1; j++) {
      System.out.print(border.getVertexY(j) + ", ");
      //System.out.print("("+border.getVertexX(j) + ", " + border.getVertexY(j) + "), "); // print out all the xy-coordinates for the path.
    }
  }
  // This for loop is to print out all the xy coordinates without a comma at the end.
  //PShape last_border = test.getChild(test.getChildCount()-1);
  //for(int j = 0 ; j < last_border.getVertexCount()-1; j++) {
      //System.out.print("("+last_border.getVertexX(j) + ", " + last_border.getVertexY(j) + "), ");
  //  }
  //System.out.print("("+last_border.getVertexX(last_border.getVertexCount()-1) + ", " + last_border.getVertexY(last_border.getVertexCount()-1) + ") ");
}

// draw() is for visualizing the test shape from the svg file.
void draw()
{
  background(255); // set the background to be white.
  shape(test, 30, 250); // draw the shape of test.
}