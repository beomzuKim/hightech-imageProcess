/* 
 * Written by Kim bZ
 * VERSION CONTROL 
 * 2022.06.13 check measurement area
 * 2022.06.14 peak noise cancelling, apply z-score
 * 2022.06.15 develop the function that control the Array for detecting Min
 * 2022.06.16 detecting Max
 * 2022.06.17 set table
 * 2022.06.20 String data set
 * 2022.06.21 control table data set
 * 2022.06.22 TEST
 * 2022.06.24 apply file format
 * 
 * 
 */
 
 close("*");
 close("FinalResults.txt");
 close("Log");
// ============================================= initialization =============================================
// ============================================= initialization =============================================
csvTable = newArray(1);
ChipID_x = newArray("-5", "-4","-4","-4","-4","-4",   "-3","-3","-3","-3","-3","-3","-3",   "-2","-2","-2","-2","-2","-2","-2",   "-1","-1","-1","-1","-1","-1","-1","-1",   "0","0","0","0","0","0","0","0","0",       "1","1","1","1","1","1","1","1",      "2","2","2","2","2","2","2",     "3","3","3","3","3","3","3",    "4","4","4","4","4",  "5");
ChipID_y = newArray("0",   "-2","-1","0","1","2",     "-3","-2","-1","0","1","2","3",         "-3","-2","-1","0","1","2","3",     "-4","-3","-2","-1","0","1","2","3",      "-4","-3","-2","-1","0","1","2","3","4",  "-4","-3","-2","-1","0","1","2","3",   "-3","-2","-1","0","1","2","3",   "-3","-2","-1","0","1","2","3", "-2","-1","0","1","2",  "0");
ImgNo = newArray("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25");
menu = "chipID_X,chipID_Y,No,value1(*),value2,value3,value4,value5,value6(*),value7(*)";

measurementArea = 400; // 
smoothValue = 3; //Smoothing
limit = 125; // limit y-value 
countNo = 19;
AnalysisCount = 1625;
csvTable = newArray(AnalysisCount);
FileNo = newArray(AnalysisCount);

for (i = 0; i < AnalysisCount; i++) {
	if (i<10){
		FileNo[i] = "00000000" + i;
	}else if (i<100){
		FileNo[i] = "0000000" + i;
	}else if (i<1000){
		FileNo[i] = "000000" + i;
	}else {
		FileNo[i] = "00000" + i;
	}
}

// ============================================= initialization =============================================
// ============================================= initialization =============================================


for (imgCount = 1; imgCount < countNo; imgCount++) {  // *** for start
 
// ************************** slecet Window & run for get array(Distance, GrayValue) *************************************
filename = FileNo[imgCount] + "HDU001.tif"; 
open("C:/Users/kim-beomzu/Desktop/OneDrive_2022-06-13/" + FileNo[imgCount] + "/" + filename );
selectWindow(filename);
makeRectangle(56, 56, measurementArea, measurementArea);

// #### 1.get Origin data ####
selectWindow(filename);
run("Plot Profile"); rename("Origin"); //(Distance-GL) Original graph
Plot.showValues("OriginTable");

// #### 2.get Smoothing data ####
selectWindow(filename);
for (i = 0; i < smoothValue; i++) {
	run("Smooth");
}

run("Plot Profile"); rename("Smooth"+"(Value:"+smoothValue+")"); //(Distance-GL) Smoothing graph
Plot.showValues("SmoothingTable");
close("*");


// ************************** Column divide & detect maximum value (10 ~ 14 point) **************************************************
selectWindow("OriginTable");
X_Origin = Table.getColumn("X");
Y_Origin = Table.getColumn("Y");

selectWindow("SmoothingTable");
X_Smooth = Table.getColumn("X");
Y_Smooth = Table.getColumn("Y");

close("OriginTable");
close("SmoothingTable");


// ********************************************* detect Maximal Value (4 ~ 7 point) *********************************************
MaxCoordinate = Array.findMaxima(Y_Smooth,1);
Array.sort(MaxCoordinate);

count = lengthOf(MaxCoordinate);
MaxCoordinate_y = newArray(count);

// delete index when the value was more bigger than "limit".
for (i = 0; i < count; i++) {
	MaxCoordinate_y[i] = Y_Smooth[MaxCoordinate[i]];
}

k0 = newArray(count); //initialization (only search second maximal value)
for (i = 0; i < count; i++) {
	 if(MaxCoordinate_y[i] < limit){
		k0[i] = MaxCoordinate[i];
	}
}

k = Array.deleteValue(k0, 0);
k_y = newArray(lengthOf(k));


// ********************************************* search y-value from x-distance ********************************************* 
for (i = 0; i < lengthOf(k); i++) {
	for (j = 0; j < 400; j++) {
		if (X_Origin[j] == k[i]) {
			k_y[i] = Y_Origin[j]; //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CHANGE ORIGIN OR SMOOTH VALUE (IMPORTANT) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ★
		}
	}
}


// ********************************************* make .csv format table  ********************************************* 
array_ky = "";
for (i = 0; i < lengthOf(k_y); i++) {
	array_ky = array_ky + "," + k_y[i];
}

csvTable[imgCount-1] = array_ky;
	
} // *** for end


 /// ********************************************* make coordinate-table and result-data-table *********************************************
coordinateCount = -1;
coordinateTable = newArray(AnalysisCount);

for (i = 0; i < lengthOf(ChipID_x); i++) {
	for (j = 0; j < lengthOf(ImgNo); j++) {
		coordinateCount = coordinateCount + 1;
		coordinateTable[coordinateCount] = ChipID_x[i] + "," + ChipID_y[i] + "," + ImgNo[j]; 
	}
}


resultTable = newArray(AnalysisCount);
for (i = 0; i < imgCount -1; i++) {  // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< need to revise imgCount ★
	resultTable[i] = coordinateTable[i] + csvTable[i];
}

close("*");


// ****************************************** concat "menu" and "result table"  **************************************************
resultTable = Array.concat(menu,resultTable);
resultTable = Array.deleteValue(resultTable, 0);
Array.show(resultTable);
selectWindow("resultTable");
setLocation(50, 50);
saveAs("results", "C:/Users/kim-beomzu/Desktop/OneDrive_2022-06-13/" + "FinalResults.txt");


// ************************************** Condition **************************************************
print("-----------------------Condition----------------------");
print("countNo: " + countNo);
print("limit: " + limit);
print("smoothingValue: " + smoothValue);
print("measurementArea:" + measurementArea + " x " + measurementArea);
print("------------------------------------------------------");
selectWindow("Log");
setLocation(750, 50);
