#include "ros/ros.h"
#include "beginner_tutorials/MultByTwo.h"

bool add(beginner_tutorials::MultByTwo::Request  &req,
         beginner_tutorials::MultByTwo::Response &res)
{
  res.output = req.input * 2;
  ROS_INFO("request: x=%ld", (long int)req.input);
  ROS_INFO("sending back response: [%ld]", (long int)res.output);


  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "mult_by_two");
  ros::NodeHandle n;

  ros::ServiceServer service = n.advertiseService("mult_by_two", add);
  ROS_INFO("Ready to multiply by two.");
  ros::spin();

  return 0;
}
