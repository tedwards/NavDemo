package com.pythonistas.timnavtest;
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import android.content.Context;
import android.location.Location;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.Toast;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.TileOverlay;
import com.google.android.gms.maps.model.TileOverlayOptions;
import com.google.android.gms.maps.model.LatLng;
import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.net.URL;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;


public class NavDemo extends FragmentActivity
{
    private static final String TAG = "-_-_-_-_TIMNAVDEMO-_-_-_-_-:";
    private GoogleMap map;
    private CameraUpdate cameraUpdate;
    private LocationManager lm;
    private Location loc;
    private NavTileProvider navtile;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        Log.d(TAG,"Start me up");
        setContentView(R.layout.main);
        map = ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map)).getMap();
        map.setMyLocationEnabled(true);
        lm = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
        Location loc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        if (loc != null){
            cameraUpdate = CameraUpdateFactory.newLatLngZoom(new LatLng(loc.getLatitude(),loc.getLongitude()), map.getMaxZoomLevel()-5);
            map.animateCamera(cameraUpdate);
        }

        loadTileOverlay();
    }

    /** Called to create the action bar menu. */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        Log.d(TAG,"Creating Menu");
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.menu_checkin:
            new CheckInTask().execute();
            break;
            
        default:
            break;
        }
        
        return true;
    }


    public void loadTileOverlay(){
        Log.d(TAG,"Loading TileOverlay");
        navtile=new NavTileProvider(256,256);
        TileOverlay tileOverlay = map.addTileOverlay(new TileOverlayOptions().tileProvider(navtile));
    }


    public void announceCheckInResult(Boolean result){
        if (result){
            Toast.makeText(this, "Checked In at current location", Toast.LENGTH_SHORT).show();
        }
        else {
            Toast.makeText(this, "Checked In FAILED!", Toast.LENGTH_LONG).show();
        }
    }

    private class CheckInTask extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... nada) {
            lm = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
            Location loc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            try {
                URL geohitURL=new URL("http://heatmaptiledemo.appspot.com/geohit?lat="+loc.getLatitude()+"&lon="+loc.getLongitude());
                HttpURLConnection urlConnection = (HttpURLConnection) geohitURL.openConnection();
                InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                urlConnection.disconnect();
                //readStream(in);
            }
            catch (IOException e){
                return false;
            } 
            finally {                
                return true;
            }
            
        }

        protected void onPostExecute(Boolean result) {
            announceCheckInResult(result);
        }
    }
}
