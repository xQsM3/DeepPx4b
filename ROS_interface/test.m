rosinit('http://HiWi-Rechner:11311/')
chatpub = rospublisher("/chatter","std_msgs/String","DataFormat","struct");
msg = rosmessage(chatpub);
msg.Data = 'hello world';

send(chatpub,msg)

