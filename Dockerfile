#This Dockerfile differs from the .devcontainer/Dockerfile because this one does not depend on VSCode to inject the
#codebase into the docker container. As such, we can use this to independently launch a docker container on the robot computer
FROM ros:foxy

# Install dependencies from apt
RUN apt-get update && apt-get install -y \
  # To use git in the container
  git \
  # pip is a package manager for Python
  python3-pip \
  # To let us sync with GitHub over SSH
  ssh-client \
  # Clean out the apt lists after `apt-get update`
  && rm -rf /var/lib/apt/lists/*

# Update pydocstyle to remove a deprecation warning when testing for PEP257
RUN pip install --upgrade pydocstyle

# Add a user so we can remote into this container with a non-root user
RUN useradd trickfire \
  # Bash will be its default shell
  --shell /bin/bash \
  # Give it a directory in /home
  --create-home \
  # Don't make a giant log file for login data, we don't care about it
  --no-log-init

# Copy all the bash customizations over to the user.
COPY .devcontainer/trickfire.bashrc /home/trickfire/.bashrc

#Copy over the codebase to the user in the urc-2023 folder
RUN mkdir /home/trickfire/urc-2023
COPY . /home/trickfire/urc-2023
