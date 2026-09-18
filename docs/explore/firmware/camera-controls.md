---
title: "Moto Mods Camera Controls"
source_url: http://developer.motorola.com/explore/firmware/camera-ext/camera-controls
source_capture: 2016 Squarespace portal
---

# Moto Mods Camera Controls

This page contains the list of Camera Controls currently in use. The full list of Controls are defined in “nuttx/include/nuttx/camera/v4l2_camera_ext_ctrls.h”. However, only subset is actually used by Camera HAL v1 on the Moto Z.

#### CAM_EXT_CID_AE_ANTIBANDING_MODE {#cam_ext_cid_ae_antibanding_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AE_ANTIBANDING_OFF
CAM_EXT_AE_ANTIBANDING_50HZ
CAM_EXT_AE_ANTIBANDING_60HZ
CAM_EXT_AE_ANTIBANDING_AUTO
```

Refer to [AE ANTIBANDING MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AE_ANTIBANDING_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported modes should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_AE_EXPOSURE_COMPENSATION {#cam_ext_cid_ae_exposure_compensation}

Integer with steps.

Refer to [AE_EXPOSURE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AE_EXPOSURE_COMPENSATION)  for details.

---

#### CAM_EXT_CID_AE_LOCK {#cam_ext_cid_ae_lock}

Boolean.

Refer to [AE_LOCK in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AE_LOCK)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AE_MODE {#cam_ext_cid_ae_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AE_MODE_OFF
CAM_EXT_AE_MODE_ON
CAM_EXT_AE_MODE_ON_AUTO_FLASH
CAM_EXT_AE_MODE_ON_ALWAYS_FLASH
CAM_EXT_AE_MODE_ON_AUTO_FLASH_REDEYE
```

Refer to [AE MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AE_MODE)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AE_TARGET_FPS_RANGE {#cam_ext_cid_ae_target_fps_range}

Integer Menu.

This is the custom made Integer menu. Each menu item consists of Integer64. The higher 32 bits contains “min fps”, and the lower 32 bits contains “max fps”.

Refer to [CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES)  for details.

Mandatory for CAMERA_EXT v1.0, although the Control is not used in HAL currently.

---

#### CAM_EXT_CID_AF_MODE {#cam_ext_cid_af_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AF_MODE_OFF
CAM_EXT_AF_MODE_AUTO
CAM_EXT_AF_MODE_MACRO
CAM_EXT_AF_MODE_CONTINUOUS_VIDEO
CAM_EXT_AF_MODE_CONTINUOUS_PICTURE
CAM_EXT_AF_MODE_EDOF
```

Refer to [AF_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AF_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported mode should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_AF_TRIGGER {#cam_ext_cid_af_trigger}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AF_TRIGGER_IDLE
CAM_EXT_AF_TRIGGER_START
CAM_EXT_AF_TRIGGER_CANCEL
```

Refer to [AF_TRIGGER in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AF_TRIGGER)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AWB_LOCK {#cam_ext_cid_awb_lock}

Boolean.

Refer to [AWB_LOCK in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AWB_LOCK)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AWB_MODE {#cam_ext_cid_awb_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AWB_MODE_OFF
CAM_EXT_AWB_MODE_AUTO
CAM_EXT_AWB_MODE_INCANDESCENT
CAM_EXT_AWB_MODE_FLUORESCENT
CAM_EXT_AWB_MODE_DAYLIGHT
CAM_EXT_AWB_MODE_CLOUDY_DAYLIGHT
CAM_EXT_AWB_MODE_TWILIGHT
CAM_EXT_AWB_MODE_SHADE
```

Refer to [AWB_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AWB_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported mode should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_EFFECT_MODE {#cam_ext_cid_effect_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_EFFECT_MODE_OFF
CAM_EXT_EFFECT_MODE_MONO
CAM_EXT_EFFECT_MODE_NEGATIVE
CAM_EXT_EFFECT_MODE_SOLARIZE
CAM_EXT_EFFECT_MODE_SEPIA
CAM_EXT_EFFECT_MODE_POSTERIZE
CAM_EXT_EFFECT_MODE_WHITEBOARD
CAM_EXT_EFFECT_MODE_BLACKBOARD
CAM_EXT_EFFECT_MODE_AQUA
```

Refer to [EFFECT_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_EFFECT_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported mode should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_SCENE_MODE {#cam_ext_cid_scene_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_SCENE_MODE_DISABLED
CAM_EXT_SCENE_MODE_FACE_PRIORITY
CAM_EXT_SCENE_MODE_ACTION
CAM_EXT_SCENE_MODE_PORTRAIT
CAM_EXT_SCENE_MODE_LANDSCAPE
CAM_EXT_SCENE_MODE_NIGHT
CAM_EXT_SCENE_MODE_NIGHT_PORTRAIT
CAM_EXT_SCENE_MODE_THEATRE
CAM_EXT_SCENE_MODE_BEACH
CAM_EXT_SCENE_MODE_SNOW
CAM_EXT_SCENE_MODE_SUNSET
CAM_EXT_SCENE_MODE_STEADYPHOTO
CAM_EXT_SCENE_MODE_FIREWORKS
CAM_EXT_SCENE_MODE_SPORTS
CAM_EXT_SCENE_MODE_PARTY
CAM_EXT_SCENE_MODE_CANDLELIGHT
CAM_EXT_SCENE_MODE_BARCODE
CAM_EXT_SCENE_MODE_HDR
```

Refer to [SCENE_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_SCENE_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported mode should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_VIDEO_STABILIZATION_MODE {#cam_ext_cid_video_stabilization_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_VIDEO_STABILIZATION_MODE_ON
CAM_EXT_VIDEO_STABILIZATION_MODE_OFF
```

Refer to [VIDEO_STABILIZATION_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_VIDEO_STABILIZATION_MODE)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_ORIENTATION {#cam_ext_cid_jpeg_orientation}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_JPEG_ORIENTATION_0
CAM_EXT_JPEG_ORIENTATION_90
CAM_EXT_JPEG_ORIENTATION_180
CAM_EXT_JPEG_ORIENTATION_270
```

Refer to [JPEG_ORIENTATION in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#JPEG_ORIENTATION)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_QUALITY {#cam_ext_cid_jpeg_quality}

Integer. (0 - 100)
Refer to [JPEG_QUALITY in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#JPEG_QUALITY)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_LENS_FACING {#cam_ext_cid_lens_facing}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_LENS_FACING_FRONT
CAM_EXT_LENS_FACING_BACK
CAM_EXT_LENS_FACING_EXTERNAL
```

Refer to [LENS_FACING in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#LENS_FACING)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_FLASH_MODE {#cam_ext_cid_flash_mode}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_FLASH_MODE_OFF
CAM_EXT_FLASH_MODE_SINGLE
CAM_EXT_FLASH_MODE_TORCH
```

Refer to [FLASH_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#FLASH_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported modes should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_FOCAL_LENGTH {#cam_ext_cid_focal_length}

Float Menu.

The list of focal lengths available on the camera in the Mod.

Refer to [FOCAL_LENGTH in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#LENS_FOCAL_LENGTH)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_SCALER_MAX_DIGITAL_ZOOM {#cam_ext_scaler_max_digital_zoom}

Float.

Refer to [SCALER_AVAILABLE_MAX_DIGITAL_ZOOM in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#SCALER_AVAILABLE_MAX_DIGITAL_ZOOM)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_SENSOR_INFO_PHYSICAL_SIZE {#cam_ext_cid_sensor_info_physical_size}

Float[2].

Refer to [SENSOR_INFO_PHYSICAL_SIZE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#SENSOR_INFO_PHYSICAL_SIZE)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_SENSOR_INFO_PIXEL_ARRAY_SIZE {#cam_ext_cid_sensor_info_pixel_array_size}

Integer[2].

Refer to [SENSOR_INFO_PIXEL_ARRAY_SIZE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#SENSOR_INFO_PIXEL_ARRAY_SIZE)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_SENSOR_INFO_ACTIVE_ARRAY_SIZE {#cam_ext_cid_sensor_info_active_array_size}

Integer[4].

Refer to [SENSOR_INFO_ACTIVE_ARRAY_SIZE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#SENSOR_INFO_ACTIVE_ARRAY_SIZE)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_SENSOR_ORIENTATION {#cam_ext_cid_sensor_orientation}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_SENSOR_ORIENTATION_0
CAM_EXT_SENSOR_ORIENTATION_90
CAM_EXT_SENSOR_ORIENTATION_180
CAM_EXT_SENSOR_ORIENTATION_270
```

Refer to [SENSOR_ORIENTATION in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#SENSOR_ORIENTATION)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_FACE_DETECTION {#cam_ext_cid_face_detection}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_CID_FACE_DETECTION_STOP
CAM_EXT_CID_FACE_DETECTION_START
```

**This is NOT Android derived control.** The Moto Mod needs to start or stop its face detection algorithm if supported. Note the face detection result must be sent over Moto Mods Camera Metadata.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_STATISTICS_INFO_MAX_FACE_COUNT {#cam_ext_cid_statistics_info_max_face_count}

Integer.

Refer to [STATISTICS_INFO_MAX_FACE_COUNT in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#STATISTICS_INFO_MAX_FACE_COUNT)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_LENS_OPTICAL_STABILIZATION_MODE {#cam_ext_cid_lens_optical_stabilization_mode}

Integer Menu. One of the following can be selected:

```
CAM_EXT_CID_LENS_OPTICAL_STABILIZATION_MODE_OFF
CAM_EXT_CID_LENS_OPTICAL_STABILIZATION_MODE_ON
```

Refer to [LENS_OPTICAL_STABILIZATION_MODE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#LENS_OPTICAL_STABILIZATION_MODE)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported modes should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_SENSOR_EXPOSURE_TIME {#cam_ext_cid_sensor_exposure_time}

Integer64.

Refer to [SENSOR_EXPOSURE_TIME in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#SENSOR_EXPOSURE_TIME)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AE_REGIONS {#cam_ext_cid_ae_regions}

Array of Integer[4]

Refer to [CONTROL_AE_REGIONS in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AE_REGIONS)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AF_REGIONS {#cam_ext_cid_af_regions}

Array of Integer[4]

Refer to [CONTROL_AF_REGIONS in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#CONTROL_AF_REGIONS)  for details.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_CAPTURE {#cam_ext_cid_capture}

Integer.

Always set from the Moto Z when a picture should be taken. The following mask(s) shall be set:

```
CAM_EXT_CID_CAPTURE_STILL_CAPTURE       = 1
CAM_EXT_CID_CAPTURE_ZSL_CAPTURE         = 1 << 2
CAM_EXT_CID_CAPTURE_RAW                 = 1 << 3
CAM_EXT_CID_CAPTURE_JPG                 = 1 << 4
```

**This is NOT Android derived control.** STILL_CAPTURE MASK shall be always set. If Mod does not create DNG file or JPG file locally, set_ctrl callback on this Control can take no action.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_AE_MODE_EXT {#cam_ext_cid_ae_mode_ext}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AE_MODE_EXT_NULL
CAM_EXT_AE_MODE_EXT_OFF_FLASH
CAM_EXT_AE_MODE_EXT_OFF_FLASH_REDEYE
```

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application to set additional AE mode not available in Android’s list.

Mandatory for CAMERA_EXT v1.0, but it’s optional to support additional modes.

---

#### CAM_EXT_CID_AF_MODE_EXT {#cam_ext_cid_af_mode_ext}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_AF_MODE_EXT_NULL
CAM_EXT_AF_MODE_EXT_INFINITY
CAM_EXT_AF_MODE_EXT_FIXED
```

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application to set additional FOCUS mode not available in Android’s list.

Mandatory for CAMERA_EXT v1.0, but it’s optional to support additional modes.

---

#### CAM_EXT_CID_SCENE_MODE_EXT {#cam_ext_cid_scene_mode_ext}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_SCENE_MODE_EXT_NULL
CAM_EXT_SCENE_MODE_EXT_AUTO_HDR
CAM_EXT_SCENE_MODE_EXT_BACKLIGHT_PORTRAIT
CAM_EXT_SCENE_MODE_EXT_CLOSEUP
CAM_EXT_SCENE_MODE_EXT_DUSK_DAWN
CAM_EXT_SCENE_MODE_EXT_FOOD
CAM_EXT_SCENE_MODE_EXT_NIGHT_LANDSCAPE
CAM_EXT_SCENE_MODE_EXT_PET_PORTRAIT
```

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application to set additional SCENE mode not available in Android’s list.

Mandatory for CAMERA_EXT v1.0, but it’s optional to support additional modes.

---

#### CAM_EXT_CID_EFFECT_MODE_EXT {#cam_ext_cid_effect_mode_ext}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_EFFECT_MODE_EXT_NULL
CAM_EXT_EFFECT_MODE_EXT_BLACK_BLUE
CAM_EXT_EFFECT_MODE_EXT_PURE
CAM_EXT_EFFECT_MODE_EXT_MIRROR
CAM_EXT_EFFECT_MODE_EXT_BUBBLE
CAM_EXT_EFFECT_MODE_EXT_NEON
CAM_EXT_EFFECT_MODE_EXT_CARTOON
CAM_EXT_EFFECT_MODE_EXT_SOFT
CAM_EXT_EFFECT_MODE_EXT_DIORAMA
```

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application to set additional EFFECT mode not available in Android’s list.

Mandatory for CAMERA_EXT v1.0, but it’s optional to support additional modes.

---

#### CAM_EXT_CID_ISO {#cam_ext_cid_iso}

Integer Menu.
One of the following can be selected:

```
CAM_EXT_ISO_AUTO
CAM_EXT_ISO_50
CAM_EXT_ISO_100
CAM_EXT_ISO_200
CAM_EXT_ISO_400
CAM_EXT_ISO_800
CAM_EXT_ISO_1600
CAM_EXT_ISO_3200
```

Refer to [SENSOR_SENSITIVITY in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#SENSOR_SENSITIVITY)  for details.

Mandatory for CAMERA_EXT v1.0. Unsupported mode should be masked by menu_skip_mask.

---

#### CAM_EXT_CID_ND_FILTER {#cam_ext_cid_nd_filter}

Integer Menu.

One of the following can be selected:

```
CAM_EXT_ND_FILTER_AUTO
CAM_EXT_ND_FILTER_ON
CAM_EXT_ND_FILTER_OFF
```

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application to control ND Filter at the camera.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_SHARPNESS {#cam_ext_cid_jpeg_sharpness}

Integer.

Parameter to adjust JPEG sharpness. Specified by the Moto Z.

Range: -2 to +2

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application. If Mod does not generate JPG file, there is no need to have this Control.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_CONTRAST {#cam_ext_cid_jpeg_contrast}

Integer.

Parameter to adjust JPEG contrast. Specified by the Moto Z.

Range: -2 to +2

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application. If Mod does not generate JPG file, there is no need to have this Control.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_SATURATION {#cam_ext_cid_jpeg_saturation}

Integer.

Parameter to adjust JPEG saturation. Specified by the Moto Z.

Range: -2 to +2

**This is NOT Android derived control.** This Control is only used by Motorola Camera Application. If Moto Mod does not generate JPG file, there is no need to have this Control.

Optional for CAMERA_EXT v1.

---

#### CAM_EXT_CID_TIME_SYNC {#cam_ext_cid_time_sync}

Integer64.

Represents the number of seconds elapsed since the Epoch, 1970-01-01 00:00:00+0000 (UTC) plus Local Timezone offset adjusted (local time in seconds).

When generating the image file on the Moto Mod and transferring via USB, this data can be used to populate fields in EXIF such as DateTime.

**This is NOT Android derived control.** This Control is used for debugging to have the Moto Z’s timestamp in log messages.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_GPS_LOCATION {#cam_ext_cid_jpeg_gps_location}

Double[2].

Set by the Moto Z for the GPS coordinate for JPG created in Moto Mod.

Refer to [JPEG_GPS_LOCATION in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#JPEG_GPS_LOCATION)  for details.

Optional for CAMERA_EXT v1.0. No need of this Control unless JPG file is created at the Mod.

---

#### CAM_EXT_CID_JPEG_GPS_TIMESTAMP {#cam_ext_cid_jpeg_gps_timestamp}

Integer64.

Set by the Core for the GPS time stamp (in UTC) of the JPG file created by the Mod.

Refer to [GpsTimestamp in the Android SDK](https://developer.android.com/reference/android/hardware/Camera.Parameters.html#setGpsTimestamp(long))  for details.

Optional for CAMERA_EXT v1.0. No need of this Control unless JPG file is created at the Mod.

---

#### CAM_EXT_CID_JPEG_GPS_PROC_METHOD {#cam_ext_cid_jpeg_gps_proc_method}

Integer64.

Set by the Moto Z to indicates the GPS Processing method in use for JPG file creation.

Refer to [GpsProcessingMethod in the Android SDK](https://developer.android.com/reference/android/hardware/Camera.Parameters.html#setGpsProcessingMethod(java.lang.String))  for details.

Optional for CAMERA_EXT v1.0. No need of this Control unless JPG file is created at the Mod.

---

#### CAM_EXT_CID_MOD_CAPS_UVC_SNAPSHOT {#cam_ext_cid_mod_caps_uvc_snapshot}

Integer[3].

Integer array whether JPEG is created in Mod and sent over USB UVC interface.

Int[0] : 0 - No JPG created at Mod.
1 - JPG is created at Mod, sent over UVC
Int[1] : USB VID used for UVC interface for JPEG transfer.
int[2] : USB PID used for UVC interface for JPEG tranfer

**This is NOT Android derived control.**

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_MOD_META_DATA_PATH {#cam_ext_cid_mod_meta_data_path}

Integer Menu.

Indicates which transport is used to send Mods Camera Metadata. Either CSI *or* GB path should be selected:

```
CAM_EXT_CID_MOD_META_DATA_PATH_NONE,  /* Not valid to use */
CAM_EXT_CID_MOD_META_DATA_PATH_CSI,
CAM_EXT_CID_MOD_META_DATA_PATH_GB
```

**This is NOT Android derived control.**

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_MOD_META_DATA_SIZE {#cam_ext_cid_mod_meta_data_size}

Integer.

If CSI is selected this Control specifies the number of lines used to carry metadata.
If Greybus is selected, this Control specifies max packet size for the metadata.

**This is NOT Android derived control.**

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_ZOOM_LOCK_1X {#cam_ext_cid_zoom_lock_1x}

Boolean.

If zoom is supported in the Moto Mod, the zoom level should be fixed to 1X while this control is set. Typically used while taking panoramic image from the multiple shots.

**This is NOT Android derived control.** Only used by Motorola Camera Application

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_MODEL_NUMBER {#cam_ext_cid_model_number}

String.

Read by the Moto Z. The model number of the Mod Camera system if any. Only used for debugging purpose.

**This is NOT Android derived control.** Only used by Motorola Camera Application

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_FIRMWARE_VERSION {#cam_ext_cid_firmware_version}

String.

Read by the Moto Z. If the camera system is running on a special ASIC, this string should represents the software version currently loaded. Used by debug as well as software update if supported.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_MANUAL_FOCUS_POSITION {#cam_ext_cid_manual_focus_position}

Integer

Range: 0 - 100

Set by Moto Z to override the focus position used by the camera. Unit is the percentage to the max focal length.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0, even if not applicable for the camera.

---

#### CAM_EXT_CID_ZOOM_LIMIT {#cam_ext_cid_zoom_limit}

Integer

Set by the Moto Z to override the maximum zoom level the camera can go up. The unit is 0.01x. 100 means 1X zoom. 1000 means 10X zoom.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0, even if not applicable for the camera.

---

#### CAM_EXT_CID_EIS_FRAME_SIZE_MAP {#cam_ext_cid_eis_frame_size_map}

Array of Integer[4]

The Moto Z supports EIS for Video Recording. If the Moto Mod wants to utilize it, it must to define this Control along with the frame resolution larger than the target video resolution. Video EIS will not be performed on the Moto Z if this Control is not declared.

Int[0], int[1] - Width and Height of EIS resolution
int[2], int[2] - Width and Height of target video resolution

The array would look like below:

```
{2304, 1296, 1920, 1080},   /* 2304x1296 resolution should be used for 1080P video out */
{1536, 864, 1280, 720},     /* 1536x864 resolution should be used for 720P video out */
```

**This is NOT Android derived control.** Only used by Motorola Applications.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_JPEG_AVAILABLE_THUMBNAIL_SIZES {#cam_ext_cid_jpeg_available_thumbnail_sizes}

Array of Integer[2]

If the Mod creates JPEG file, this Control indicate the list of the thumbnail image embedded in the picture.

Int[0] - Width of the thumbnail
Int[1] - Height of the thumbnail

Refer to [JPEG_AVAILABLE_THUMNAIL_SIZES in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics.html#JPEG_AVAILABLE_THUMBNAIL_SIZES)  for details.

Mandatory for CAMERA_EXT v1.0, even if JPEG is not created by the Moto Mod. The value will be ignored if JPEG is created by the Moto Z.

---

#### CAM_EXT_CID_JPEG_THUMBNAIL_SIZE_INDEX {#cam_ext_cid_jpeg_thumbnail_size_index}

Integer

Set by the Moto Z. Index to the AVAILABLE_THUMBNAIL_SIZES array to specify which size should be used for JEPG file creation.

Refer to [JPEG_THUMNAIL_SIZE in the Android SDK](https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html#JPEG_THUMBNAIL_SIZE)  for details.

Mandatory for CAMERA_EXT v1.0, even if JPEG is not created by the Moto Mod. Ignore the value if not supported.

---

#### CAM_EXT_CID_PHONE_VERSION {#cam_ext_cid_phone_version}

String

The Moto Z sets it’s version string so it is embedded in JPEG EXIF created by the Mod.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0, even if JPEG is not created by the Moto Mod. Ignore the value if not supported.

---

#### CAM_EXT_CID_SUPPLEMENTAL_KEY_MASK {#cam_ext_cid_supplemental_key_mask}

Integer

If the Moto Mod has the hardware keys, this Control indicates availability to the Moto Z. The integer value consists of bit mask of each pre-defined hardware keys.

The masks are defined below. The “_EVT” postfix means the actual key event would get propagated to Camera Application or not.

```
CAM_EXT_HW_KEY_POWER          = 1
CAM_EXT_HW_KEY_POWER_EVT      = 1 << 1
CAM_EXT_HW_KEY_ZOOM_IN        = 1 << 2
CAM_EXT_HW_KEY_ZOOM_IN_EVT    = 1 << 3
CAM_EXT_HW_KEY_ZOOM_OUT       = 1 << 4
CAM_EXT_HW_KEY_ZOOM_OUT_EVT   = 1 << 5
CAM_EXT_HW_KEY_FOCUS          = 1 << 6
CAM_EXT_HW_KEY_FOCUS_EVT      = 1 << 7
CAM_EXT_HW_KEY_CAMERA         = 1 << 8
CAM_EXT_HW_KEY_CAMERA_EVT     = 1 << 9
```

Example: mask value = 0b0011010100 means ZOOM keys and FOCUS key are present. Zoom key events are consumed in Moto Mod. But the Focus key event would be sent up to the application.

**This is NOT Android derived control.** Only used by Motorola Applications.

Optional for CAMERA_EXT v1.0

---

#### CAM_EXT_CID_GROUP_IND {#cam_ext_cid_group_ind}

Integer

Value: 0 means Grouping OFF, 1 means Grouping ON

The Moto Z may set more than one control at a time assuming those parameters are updated in very close timing. The GROUP_IND indicates the beginning and the end of series of “set_ctrl” call to be executed together. The Moto Mod may cache the values in “set_ctrl” until the “Grouping OFF” arrives before updating its camera system.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0. Ignore the value if not applicable.

---

#### CAM_EXT_CID_VIDEO_RECORD_HINT {#cam_ext_cid_video_record_hint}

Boolean

Indicates the Moto Z is recording the video from the currently running stream. The Moto Mod may behave differently while video recording is in progress. (like slow zooming etc.) It is up to Moto Mod how to consume this Control value.

**This is NOT Android derived control.**

Mandatory for CAMERA_EXT v1.0. Ignore the value if not applicable.

---

#### CAM_EXT_CID_ZSL_BUFFER_DEPTH {#cam_ext_cid_zsl_buffer_depth}

Integer

Set by the Moto Z. If ZSL capture is executed by the Moto Mod, this Control specify the depth of the ZSL buffer to use.

**This is NOT Android derived control.** Only used by Motorola Applications.

Mandatory for CAMERA_EXT v1.0. Ignore the value if not applicable.

---

#### CAM_EXT_CID_RAW_TO_YUV_GAIN {#cam_ext_cid_raw_to_yuv_gain}

Float[3]

The Moto Z will perform RAW to YUV color conversion In case RAW sensor is used. This Control is used to adjust gain of R, G and B channel while color conversion is in progress.

Float[0] - R channel gain. 1.0f means no adjustment.
Float[1] - G channel gain. 1.0f means no adjustment.
Float[2] - B channel gain. 1.0f means no adjustment.

Example: {1.0f, 0.92f, 1.25f} Decrease G gain (x 0.92). Increase B gain (x 1.25)

**This is NOT Android derived control.**

Optional for CAMERA_EXT v1.0.
