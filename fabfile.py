from fabric.api import put, task, cd, run
from fabric.operations import local
import os

@task
def load_data(local_dir, graph):
    virtuoso_dir = "~/virtuoso/"
    remote_dir = os.path.join(virtuoso_dir, "last_load")
    run("mkdir -p last_load")
    local("tar -cvzf /tmp/data.tgz %s/*" % remote_dir)
    with cd(remote_dir):
        run("rm -f *.rdf")
        put("/tmp/data.tgz", remote_dir)
        run("tar -xvzf data.tgz")
        run("rm data.tgz")
        #run("~/RDFClip/scripts/load_data -g %s -d %s" % (graph, os.path.join(virtuoso_dir))
