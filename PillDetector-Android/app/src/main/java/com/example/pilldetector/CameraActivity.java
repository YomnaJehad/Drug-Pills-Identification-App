package com.example.pilldetector;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.PorterDuff;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.renderscript.RenderScript;
import android.speech.tts.TextToSpeech;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.JSONObjectRequestListener;
import com.androidnetworking.interfaces.UploadProgressListener;

import static android.widget.Toast.LENGTH_SHORT;


public class CameraActivity extends AppCompatActivity {

    static final int REQUEST_IMAGE_CAPTURE = 1;
    String CurrentPhotoPath;
    ImageView cameraView;
    Button cameraCapture;
    Button checkPill;
    Button reCapture;
    TextToSpeech t1;
    LinearLayout linearLayout;
    String base64Image;
    final String[] response = new String[1];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        android.support.v7.app.ActionBar actionBar = getSupportActionBar();
        actionBar.setBackgroundDrawable(new ColorDrawable(Color.WHITE));
        actionBar.setTitle(Html.fromHtml("<font color=\"#2764a5\">" + getString(R.string.app_name) + "</font>"));

        t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t1.setLanguage(Locale.US);
                }
            }
        });

        cameraView = this.findViewById(R.id.imageView1);
        cameraCapture = this.findViewById(R.id.cameraBtn);
        checkPill = this.findViewById(R.id.checkPill);
        reCapture = this.findViewById(R.id.retake);
        linearLayout = this.findViewById(R.id.linearLayout);

        cameraCapture.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dispatchTakePictureIntent();
//
            }
        });

        reCapture.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dispatchTakePictureIntent();
            }
        });

        checkPill.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendPost("https://pill-detector.herokuapp.com/pill/");
            }
        });
    }


    private void dispatchTakePicturesIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(this,
                        "com.example.pilldetector",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
            }
        }
    }

    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        CurrentPhotoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {

            File file = new File(CurrentPhotoPath);

            try {
                ExifInterface ei = new ExifInterface(CurrentPhotoPath);
                int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION,
                        ExifInterface.ORIENTATION_UNDEFINED);

                Bitmap imageBitmap = MediaStore.Images.Media
                        .getBitmap(this.getContentResolver(), Uri.fromFile(file));

                switch(orientation) {

                    case ExifInterface.ORIENTATION_ROTATE_90:
                        imageBitmap = rotateImage(imageBitmap, 90);
                        break;

                    case ExifInterface.ORIENTATION_ROTATE_180:
                        imageBitmap = rotateImage(imageBitmap, 180);
                        break;

                    case ExifInterface.ORIENTATION_ROTATE_270:
                        imageBitmap = rotateImage(imageBitmap, 270);
                        break;

                    case ExifInterface.ORIENTATION_NORMAL:
                }

                cameraView.setImageBitmap(imageBitmap);

                ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                imageBitmap.compress(Bitmap.CompressFormat.JPEG, 30, bytes);
                byte[] byteArray = bytes.toByteArray();

                base64Image = Base64.encodeToString(byteArray, Base64.DEFAULT);

                cameraCapture.setVisibility(View.INVISIBLE);
                linearLayout.setVisibility(View.VISIBLE);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static Bitmap rotateImage(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(),
                matrix, true);
    }

    public void sendPost(final String urlAddress) {

        final ProgressDialog progressDoalog = new ProgressDialog(CameraActivity.this);
        progressDoalog.setMax(100);
        progressDoalog.setMessage("Please wait...");
        progressDoalog.setTitle("Checking");
        progressDoalog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        Drawable drawable = new ProgressBar(this).getIndeterminateDrawable().mutate();
        drawable.setColorFilter(Color.parseColor("#2764a5"),
                PorterDuff.Mode.SRC_IN);
        progressDoalog.setIndeterminateDrawable(drawable);
        progressDoalog.setCancelable(false);
        progressDoalog.show();


        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {

                    AndroidNetworking.upload(urlAddress)
                            //.addMultipartFile("image",sourceFile)
                            .addMultipartParameter("img", base64Image)
                            .build()
                            .setUploadProgressListener(new UploadProgressListener() {
                                @Override
                                public void onProgress(long bytesUploaded, long totalBytes) {
                                    // do anything with progress

                                }
                            })
                            .getAsJSONObject(new JSONObjectRequestListener() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    // do anything with response
//                                    Toast.makeText(getApplicationContext(),"Posted",LENGTH_SHORT).show();
                                    final String name = response.optString("name");
                                    final String desc = response.optString("description");
                                    t1.speak(name , TextToSpeech.QUEUE_FLUSH, null, null);
//                                    t1.speak(desc, TextToSpeech.QUEUE_FLUSH, null, null);

                                    AlertDialog dialog = new AlertDialog.Builder(CameraActivity.this)
                                            .setTitle(name)
                                            .setMessage(desc)
                                            .setPositiveButton(android.R.string.ok, new DialogInterface.OnClickListener() {

                                                @Override
                                                public void onClick(DialogInterface dialog, int which) {
                                                    dialog.dismiss();
                                                }
                                            }).create();
                                    dialog.show();

                                    runOnUiThread(new Runnable(){
                                        public void run() {
                                            saveImageFirebase(name + " : " + desc);
                                            progressDoalog.dismiss();
                                        }
                                    });
                                }
                                @Override
                                public void onError(final ANError error) {
                                    // handle error
                                    System.out.println(error.getErrorDetail());
                                    System.out.println(error.getErrorBody());
                                    System.out.println(error.getErrorCode());
                                    t1.speak("Sorry Error Occurred", TextToSpeech.QUEUE_FLUSH, null, null);
                                    runOnUiThread(new Runnable(){
                                        public void run() {
                                            saveImageFirebase(error.getErrorBody());
                                            progressDoalog.dismiss();
                                        }
                                    });
                                }
                            });

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        thread.start();

    }

    public void saveImageFirebase(final String name){
//        final ProgressDialog progressDoalog = new ProgressDialog(CameraActivity.this);
//        progressDoalog.setMax(100);
//        progressDoalog.setMessage("Please wait...");
//        progressDoalog.setTitle("Checking");
//        progressDoalog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
//        Drawable drawable = new ProgressBar(this).getIndeterminateDrawable().mutate();
//        drawable.setColorFilter(Color.parseColor("#2764a5"),
//                PorterDuff.Mode.SRC_IN);
//        progressDoalog.setIndeterminateDrawable(drawable);
//        progressDoalog.setCancelable(false);
//        progressDoalog.show();


        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {

                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("name", name);
                        jsonObject.put("img", base64Image);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    AndroidNetworking.post("https://testing-894c8.firebaseio.com/images.json")
                            //.addMultipartFile("image",sourceFile)
                            .addJSONObjectBody(jsonObject)
                            .build()
                            .setUploadProgressListener(new UploadProgressListener() {
                                @Override
                                public void onProgress(long bytesUploaded, long totalBytes) {
                                    // do anything with progress

                                }
                            })
                            .getAsJSONObject(new JSONObjectRequestListener() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    // do anything with response
//                                    Toast.makeText(getApplicationContext(),"Posted",LENGTH_SHORT).show();
                                    t1.speak("Done Uploading Picture", TextToSpeech.QUEUE_FLUSH, null, null);

//                                    t1.speak(name , TextToSpeech.QUEUE_FLUSH, null, null);
//                                    t1.speak(desc, TextToSpeech.QUEUE_FLUSH, null, null);



                                    runOnUiThread(new Runnable(){
                                        public void run() {
//                                            progressDoalog.dismiss();
                                        }
                                    });
                                }
                                @Override
                                public void onError(ANError error) {
                                    // handle error
                                    System.out.println(error.getErrorDetail());
                                    System.out.println(error.getErrorBody());
                                    System.out.println(error.getErrorCode());
                                    t1.speak("Sorry Error Occurred in sending to Firebase", TextToSpeech.QUEUE_FLUSH, null, null);
                                    runOnUiThread(new Runnable(){
                                        public void run() {
//                                            progressDoalog.dismiss();
                                        }
                                    });
                                }
                            });

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        thread.start();
    }
}
