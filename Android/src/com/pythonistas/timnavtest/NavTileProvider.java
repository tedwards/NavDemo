package com.pythonistas.timnavtest;

import android.content.Context;
import android.graphics.Bitmap;  
import android.graphics.BitmapFactory;  
import android.util.Log;
import com.google.android.gms.maps.model.UrlTileProvider;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.net.URL;
import java.net.MalformedURLException;

public class NavTileProvider extends UrlTileProvider
{
    private static final String TAG = "-_-_-_-_TIMNAVDEMO-_NAVTILEPROVIDER-_-_-_-:";
    private Bitmap singleBMP;
    private Bitmap doubleBMP;
    private Bitmap multiBMP;
    private byte[] singleData;
    private byte[] doubleData;
    private byte[] multiData;
    private Context context;

    public NavTileProvider (int width, int height)
    {
        super(width, height);
    }


    public URL getTileUrl(int x, int y, int zoom) 
    {
        Log.d(TAG, "Providing URL::"+"http://heatmaptiledemo.appspot.com/tile?x="+x+"&y="+y+"&zoom="+zoom);
        try{
            URL loc=new URL("http://heatmaptiledemo.appspot.com/tile?x="+x+"&y="+y+"&zoom="+zoom);
            return loc;
        } 
        catch (MalformedURLException e){
            Log.d(TAG, "MALFORMED URL");
            return null;
        }

    }
}
