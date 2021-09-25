# dbd_bloodweb_python
Program that levels up bloodweb in Dead by Daylight. My program detects neighbour nodes, that can be leveled up, then sorts them by rarity and selects most rare/most common.


CAREFUL: use this program at your own risk. I was told that i can't modify game files, but nobody tells anything about moving mouse.


How to use program: 

1) Install Python from https://www.python.org/ .
2) Download folder with source code and unpack it.
3) Install requirements by running "pip install -r requirements.txt" in folder with source code.
  If you get error message, try "pip install wheel" and "pip install -r requirements.txt" again.
4) Run calibration.py script and switch window to DbD with opened bloodweb.
  Prefferably use bloodweb with no leveled up nodes of all colors. If program doesn't click inside circles, calibrate again.
  Original screenshot:
  ![Original](https://user-images.githubusercontent.com/35243176/134715338-8e9c87c7-454f-42dd-b52f-e8d82f3134a2.jpg)
  1. Crop your screen to get area with bloodweb inside. After you get desired image, click on image window and press ESC.
  ![calibrate_screen_dimensions](https://user-images.githubusercontent.com/35243176/134711965-c9c541aa-e5db-4204-bd46-a0138b376f49.png)
  2. Filter image by color to get neighbour circles. 
  ![neighbours_color](https://user-images.githubusercontent.com/35243176/134714114-3b671cc6-4127-47fd-a1ba-2707e1fec9df.png)
  3. Move sliders, so you are left with next image.
  ![circle_detection](https://user-images.githubusercontent.com/35243176/134714637-917a86b0-5f12-41c8-b96c-95cd69bb139b.png)
  4. Same filtering by color for iridescent/purple/green/yellow nodes. There are many brown elements on screen, so filtering by brown doesn't do much.
  
  
  ![filter_by_color](https://user-images.githubusercontent.com/35243176/134716164-4a0075b6-1c6d-4905-ac28-0cd16a84d54f.png)


 Run main.py when you want to spend bloodpoints. When you want to stop, hold your mouse in top left corner for several seconds or Alt-Tab and stop execution.

 Known issues:
    1) Some Nemesis addons have very much white pixels inside circle so there are issues with determination of their quality.
