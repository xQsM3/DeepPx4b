function talker()
    try
        %change adress to whatever roscore ROS_MASTER_URI says
        % https://de.mathworks.com/help/ros/ug/connect-to-a-ros-network.html
        rosinit('http://HiWi-Rechner:11311/') 
        roscore = ros.Core(11311) %assuming port 11311 is open!
        cam_node = ros.Node('cam_publisher','http://HiWi-Rechner:11311/');
    catch e
        fprintf(1,'The identifier was:\n%s',e.identifier);
        fprintf(1,'Error while init rosnode cam_node:\n%s',e.message);
        global cam_node
    end

    publisher = ros.Publisher(cam_node,'/camera_front/rgb/image_raw','sensor_msgs/Image');
    msg_im_pub = rosmessage(publisher)
    
    % Read some image here , replace later with Unreal Engine Camera Image
    image = imread('koala.jpg'); 
    [height,width,channels] = size(image); 
    image = permute(image,[3 2 1]); % Flip dimensions 
    image = image(:); % Vectorize
    % Populate image message
    msg_im_pub.Step = width * channels;
    msg_im_pub.Width = width;
    msg_im_pub.Height = height;
    
    msg_im_pub.Encoding = 'rgb8';
    msg_im_pub.Data = image;
    
    %stream.buffer().clear(); % Clear java buffer
    r = rosrate(30)
    
    while true
        time = r.TotalElapsedTime;
        send(publisher,msg_im_pub)
        waitfor(r);
    end
end


