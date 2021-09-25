import os 
import pkg_resources

def latest(component: str, snapshot: bool):
    versions = pkg_resources.resource_listdir(__name__,component)
    if snapshot:
        versions = [a for a in versions if a.endswith('-SNAPSHOT.yaml')]
    else: 
        versions = [a for a in versions if not a.endswith('-SNAPSHOT.yaml')]
    versions.sort(reverse=True)
    if len(versions)==0:
        print('There are no yaml for this component')
        exit(1)
    return versions[0][:-5] 

def extract_file(component: str, version: str):     
    if version=='latest-SNAPSHOT':
        version = latest(component=component,snapshot=True)
    elif version=='latest':
        version = latest(component=component,snapshot=False)

    if not pkg_resources.resource_exists(__name__,component+'/'+version+'.yaml'):
        print('## ERROR component {}:'.format(component))
        files = pkg_resources.resource_listdir(__name__,component)
        if len(files)==0:
            print('there are no yaml for this component')
            exit(1)
        print('Current versions are:')
        [print(a) for a in files]
        exit(1)

    file = pkg_resources.resource_filename(__name__, component+'/'+version+'.yaml')

    return os.path.abspath(file)


def folder2_component(version: str):
    return extract_file(component='folder2', version=version)

def folder1_component(version: str):
    return extract_file(component='folder1', version=version)


if __name__=='__main__':
    print(folder2_component(version='latest'))
    print(folder1_component(version='8.0.8-SNAPSHOT'))
