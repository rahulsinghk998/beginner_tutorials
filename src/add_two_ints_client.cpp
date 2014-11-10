#include "ros/ros.h"
#include "beginner_tutorials/AddTwoInts.h"
#include "beginner_tutorials/MultByTwo.h"
#include "beginner_tutorials/Num.h"
#include <cstdlib>

void chatterCallback(const beginner_tutorials::Num::ConstPtr& msg)
{
  long adder = 0;
  ros::NodeHandle n;
  ros::ServiceClient client1 = n.serviceClient<beginner_tutorials::AddTwoInts>("add_two_ints");


  beginner_tutorials::Num value_to_send;

  beginner_tutorials::AddTwoInts srv;

  srv.request.a = msg->num;  //long int)data.c_str();
  srv.request.b = msg->num;  //->data.c_str();


  if (client1.call(srv))
  {
    ROS_INFO("Sum: %ld", (long int)srv.response.sum);
    adder = srv.response.sum;
    //value_to_send.score = adder;
  }
  else
  {
    ROS_ERROR("Failed to call service add_two_ints");
  }

  ros::ServiceClient client2 = n.serviceClient<beginner_tutorials::MultByTwo>("mult_by_two");
  beginner_tutorials::MultByTwo service;
  service.request.input = adder;
  //value_to_send.score = adder;

  if (client2.call(service))
  {
    ROS_INFO("Doubled Sum: %ld", (long int)service.response.output);

  }
  else
  {
    ROS_ERROR("Failed to call service mult_by_two");
  }

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "add_two_ints_client");

  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);

  ros::spin();

  return 0;
}
