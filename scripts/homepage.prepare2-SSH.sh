# remove saved keys
sudo mv /Users/olehkrupko/.ssh/known_hosts ~/Desktop/known_hosts

# putting keys
ssh-keygen -R krupko.space  # in case there are key issues
ssh-keygen  # generate keys
ssh-copy-id pi@krupko.space  # upload keys to server
ssh-copy-id pi@192.168.1.201 -f  # in case of issues

# connecting
ssh -p 8022 pi@krupko.space