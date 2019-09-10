
#
CUDA_VISIBLE_DEVICES=7 python main.py --env BipedalWalkerHardcore-v2 --max_episode_length 1000 --trajectory_length 10 --debug --visualize

#python main.py --env Pendulum-v0 --max_episode_length 1000 --trajectory_length 10 --debug --visualize