// Camera libraries
#include "driver/rtc_io.h"
#include "esp_camera.h"
#include "soc/rtc_cntl_reg.h"
#include "soc/soc.h"

// MicroSD Libraries
#include <string>

#include "FS.h"
#include "SD_MMC.h"
#include "SPI.h"

// Pin definitions for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

// Counter for picture number
unsigned int pictureCount = 0;

#define DELAY 15 * 1000
#define STACK_PICS 5

bool saveFileNumber(size_t num);
size_t getFileNumber();
bool logFile(String str);

typedef struct {
    uint32_t filesize;
    uint32_t reserved;
    uint32_t fileoffset_to_pixelarray;
    uint32_t dibheadersize;
    int32_t width;
    int32_t height;
    uint16_t planes;
    uint16_t bitsperpixel;
    uint32_t compression;
    uint32_t imagesize;
    uint32_t ypixelpermeter;
    uint32_t xpixelpermeter;
    uint32_t numcolorspallette;
    uint32_t mostimpcolor;
} bmp_header_t;

void configESPCamera() {
    camera_config_t config;

    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer   = LEDC_TIMER_0;
    config.pin_d0       = Y2_GPIO_NUM;
    config.pin_d1       = Y3_GPIO_NUM;
    config.pin_d2       = Y4_GPIO_NUM;
    config.pin_d3       = Y5_GPIO_NUM;
    config.pin_d4       = Y6_GPIO_NUM;
    config.pin_d5       = Y7_GPIO_NUM;
    config.pin_d6       = Y8_GPIO_NUM;
    config.pin_d7       = Y9_GPIO_NUM;
    config.pin_xclk     = XCLK_GPIO_NUM;
    config.pin_pclk     = PCLK_GPIO_NUM;
    config.pin_vsync    = VSYNC_GPIO_NUM;
    config.pin_href     = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn     = PWDN_GPIO_NUM;
    config.pin_reset    = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;  // Choices are YUV422, GRAYSCALE, RGB565, JPEG

    // Select lower framesize if the camera doesn't support PSRAM
    if (psramFound()) {
        config.frame_size   = FRAMESIZE_UXGA;  // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
        config.jpeg_quality = 10;              // 10-63 lower number means higher quality
        config.fb_count     = 2;
    } else {
        config.frame_size   = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count     = 1;
    }

    // Initialize the Camera
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x", err);
        logFile("Camera init failed with error");
        return;
    }

    // Camera quality adjustments
    sensor_t *s = esp_camera_sensor_get();

    s->set_brightness(s, 0);                  // BRIGHTNESS (-2 to 2)
    s->set_contrast(s, 0);                    // CONTRAST (-2 to 2)
    s->set_saturation(s, 0);                  // SATURATION (-2 to 2)
    s->set_special_effect(s, 0);              // SPECIAL EFFECTS (0 - No Effect, 1 - Negative, 2 - Grayscale, 3 - Red Tint, 4 - Green Tint, 5 - Blue Tint, 6 - Sepia)
    s->set_whitebal(s, 1);                    // WHITE BALANCE (0 = Disable , 1 = Enable)
    s->set_awb_gain(s, 1);                    // AWB GAIN (0 = Disable , 1 = Enable)
    s->set_wb_mode(s, 0);                     // WB MODES (0 - Auto, 1 - Sunny, 2 - Cloudy, 3 - Office, 4 - Home)
    s->set_exposure_ctrl(s, 1);               // EXPOSURE CONTROLS (0 = Disable , 1 = Enable)
    s->set_aec2(s, 0);                        // AEC2 (0 = Disable , 1 = Enable)
    s->set_ae_level(s, 0);                    // AE LEVELS (-2 to 2)
    s->set_aec_value(s, 300);                 // AEC VALUES (0 to 1200)
    s->set_gain_ctrl(s, 1);                   // GAIN CONTROLS (0 = Disable , 1 = Enable)
    s->set_agc_gain(s, 0);                    // AGC GAIN (0 to 30)
    s->set_gainceiling(s, (gainceiling_t)0);  // GAIN CEILING (0 to 6)
    s->set_bpc(s, 0);                         // BPC (0 = Disable , 1 = Enable)
    s->set_wpc(s, 1);                         // WPC (0 = Disable , 1 = Enable)
    s->set_raw_gma(s, 1);                     // RAW GMA (0 = Disable , 1 = Enable)
    s->set_lenc(s, 1);                        // LENC (0 = Disable , 1 = Enable)
    s->set_hmirror(s, 0);                     // HORIZ MIRROR (0 = Disable , 1 = Enable)
    s->set_vflip(s, 0);                       // VERT FLIP (0 = Disable , 1 = Enable)
    s->set_dcw(s, 1);                         // DCW (0 = Disable , 1 = Enable)
    s->set_colorbar(s, 0);                    // COLOR BAR PATTERN (0 = Disable , 1 = Enable)
}

void initMicroSDCard() {
    gpio_pulldown_dis(GPIO_NUM_13);  // Fix for 1 bit
    gpio_pullup_en(GPIO_NUM_13);

    // Start the MicroSD card
    Serial.println("Mounting MicroSD Card");
    if (!SD_MMC.begin("/sdcard", true)) {
        Serial.println("Failed to mount SD card");
        logFile("Failed to mount SD card");
        return;
    }

    // Turn off the led
    pinMode(4, OUTPUT);
    digitalWrite(4, LOW);

    // Check if all went well
    uint8_t cardType = SD_MMC.cardType();
    if (cardType == CARD_NONE) {
        Serial.println("No SD Card found");
        logFile("No SD Card found");
        return;
    }
}

bool saveFile(String path, uint8_t *buff, size_t len) {
    // Save picture to microSD card
    fs::FS &fs = SD_MMC;
    File file  = fs.open(path.c_str(), FILE_WRITE);
    if (!file) {
        Serial.println("Failed to open file in write mode");
        logFile("Failed to open file in write mode");
        file.close();
        return false;
    } else {
        file.write(buff, len);  // payload (image), payload length
        Serial.printf("Saved file to path: %s\n", path.c_str());
    }
    // Close the file
    file.close();
    return true;
}

bool saveFileNumber(size_t num) {
    String path = "/fileNum.txt";
    fs::FS &fs  = SD_MMC;
    File file   = fs.open(path.c_str(), FILE_WRITE);

    if (!file) {
        Serial.println("Failed to open log file in write mode");
        file.close();
        return false;
    } else {
        file.print(num);
    }
    // Close the file
    file.close();
    return true;
}

size_t getFileNumber() {
    String path = "/fileNum.txt";
    fs::FS &fs  = SD_MMC;
    File file   = fs.open(path.c_str(), FILE_READ);
    String num;

    if (!file) {
        Serial.println("Failed to open log file to read");
        file.close();
        return 0;
    } else {
        num = file.readString();
    }
    // Close the file
    file.close();
    return num.toInt();
}

bool logFile(String str) {
    String path = "/log.txt";
    fs::FS &fs  = SD_MMC;
    File file   = fs.open(path.c_str(), FILE_APPEND);
    if (!file) {
        Serial.println("Failed to open log file in append mode");
        file.close();
        return false;
    } else {
        file.println(str);
    }
    // Close the file
    file.close();
    return true;
}

void setup() {
    // Disable brownout detector
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

    // Start Serial Monitor
    Serial.begin(115200);

    // Initialize the MicroSD
    Serial.print("Initializing the MicroSD card module... ");
    initMicroSDCard();

    // Initialize the camera
    Serial.print("Initializing the camera module...");
    logFile("Initializing the camera module on picture number: " + getFileNumber());
    configESPCamera();
    Serial.println("Camera OK!");

    // Get the num file
    pictureCount = getFileNumber();
    Serial.print("Delay Time = ");

    Serial.print(DELAY);
    Serial.println(" ms");
}

void loop() {
    for (size_t i = 0; i < STACK_PICS; i++) {
        // Setup frame buffer
        camera_fb_t *fb = esp_camera_fb_get();

        if (!fb) {
            Serial.println("Camera capture failed");
            logFile("Camera capture failed " + pictureCount);
        }

        // String path;  //= "/image" + String(pictureCount++) + ".jpg";
        char path[12];
        sprintf(path, "/%06d.jpg", pictureCount++);
        saveFile(path, fb->buf, fb->len);

        // Return the frame buffer back to the driver for reuse
        esp_camera_fb_return(fb);
    }
    saveFileNumber(pictureCount);

    // Delay for specified period
    delay(DELAY);
}