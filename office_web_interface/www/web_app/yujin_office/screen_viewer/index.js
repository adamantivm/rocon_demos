var ros = new ROSLIB.Ros();

var defaultUrL = rocon_interactions.rosbridge_uri;
var screen_id = rocon_interactions.parameters['screen'];
var config_values = {};

var res_path = './video/'
config_values['res_path'] = './video/';
config_values['screen_id'] = screen_id;

// var robot2 = rocon_interactions.parameters['robot2'];
// var robot3 = rocon_interactions.parameters['robot3'];

// var viewer;
// var gridClient;
// var circle_region_poller;
// var ar_region_poller;
// var annotator;

var show_video_sub_topic_name = '/show_video'
var show_video_sub_topic_type = 'simple_media_msgs/ShowVideo'


delivery_status_list = {
"10" : "IDLE",
"20" : "GO_TO_FRONTDESK",
"30" : "ARRIVAL_AT_FRONTDESK",
"40" : "WAITING_FOR_FRONTDESK",
"51" : "GO_TO_RECEIVER",
"52" : "ARRIVAL_AT_RECEIVER",
"53" : "WAITING_CONFIRM_RECEIVER",
"54" : "COMPLETE_DELIVERY",
"60" : "COMPLETE_ALL_DELIVERY",
"70" : "RETURN_TO_DOCK",
"80" : "COMPELTE_RETURN",
"-10" : "ERROR"
}


$().ready(function(e) {
    $('.video-screen-viewer').css("height",$( window ).height()).css("width",$( window ).width());
    initRos();
    initConfig(config_values);
});

function initRos()
{
  settingROSCallbacks();
  ros.connect(defaultUrL);
  $(".rosbridge-ip-info").html(defaultUrL);
}

function settingROSCallbacks()                      
{
  ros.on('connection',function() {
    console.log("Connected");
    $(".rosbridge-connection-info").html("Connection");
    // subscribe to order list                                                       
    
    var showvideo_listener = new ROSLIB.Topic({
      ros : ros,
      name : show_video_sub_topic_name,
      messageType: show_video_sub_topic_type
      });
    showvideo_listener.subscribe(processShowVideo);
    }
  );
  ros.on('error',function(e) {
    console.log("Error!",e);
    $(".rosbridge-connection-info").html("Error: "+ e);
  }
  );
                                               
  ros.on('close',function() {
    console.log("Connection Close!");
    $(".rosbridge-connection-info").html("Connection Close!");
  }
  );

}

function processShowVideo(msg) {
  console.log(msg);
  console.log(config_values);
  if (config_values['screen_id']  == msg.screen_id){
    console.log("screnn id corrected");
    $(".video-screen-viewer").attr("src",config_values['res_path']+msg.video_url);
  }
  else{
    console.log("screnn id did not correct");
  }
}
  