#include <SPI.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library

#define TFT_CS        10
#define TFT_RST        8 // Or set to -1 and connect to Arduino RESET pin
#define TFT_DC         9

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  Serial.begin(9600);
  tft.initR(INITR_BLACKTAB); // Init ST7735R chip, green tab
  //tft.fillScreen(ST77XX_BLACK);
  tft.setRotation(1); // set display orientation
  tft.fillScreen(ST77XX_WHITE);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.println(data);
    if (data == "Initialising!") {
      tft.fillScreen(ST77XX_WHITE);
      print_text(3,55,"Initialising!",2,ST77XX_BLUE);
    }
    else if (data == "Please scan passport!") {
      tft.fillScreen(ST77XX_WHITE);
      print_text(15,40,"Please scan",2,ST77XX_ORANGE);
      print_text(30,70,"passport!",2,ST77XX_ORANGE);
    }
    else if (data == "Dispensing") {
      tft.fillScreen(ST77XX_WHITE);
      print_text(20,55,"Dispensing",2,ST77XX_BLACK);
      delay(500);
      tft.fillScreen(ST77XX_WHITE);
      print_text(14,55,"Dispensing.",2,ST77XX_BLACK);
      delay(500);
      tft.fillScreen(ST77XX_WHITE);
      print_text(8,55,"Dispensing..",2,ST77XX_BLACK);
      delay(500);
      tft.fillScreen(ST77XX_WHITE);
      print_text(2,55,"Dispensing...",2,ST77XX_BLACK);
      delay(500);
    }
    else if (data == "Please hold!") {
      tft.fillScreen(ST77XX_WHITE);
      print_text(20,55,"Please hold!",2,ST77XX_BLACK);
    }
    else {
      tft.fillScreen(ST77XX_WHITE);
      print_text(30,55,"Error!",3,ST77XX_RED);
    }
  }
}
  
//  tft.fillScreen(ST77XX_BLACK);
//  tft.fillRoundRect(25, 10, 78, 60, 8, ST77XX_WHITE);
//  tft.fillTriangle(42, 20, 42, 60, 90, 40, ST77XX_RED);
//  delay(5000);
//  
//  tft.fillScreen(ST77XX_CYAN);
//  tft.drawRect(5,5,120,120,ST77XX_RED);
//  tft.drawFastHLine(5,60,120,ST77XX_RED);
//  tft.drawFastVLine(60,5,120,ST77XX_RED);
//  delay(5000);


void print_text(byte x_pos, byte y_pos, char *text, byte text_size, uint16_t color) {
  tft.setCursor(x_pos, y_pos);
  tft.setTextSize(text_size);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}
