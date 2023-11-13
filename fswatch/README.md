# 2023-08

Event queue overflow.


Want

    fswatch -Lrtux --event-flag-separator=, --event=Created --event=Updated --event=MovedTo --event=Removed .

    inotifywait -mrq --timefmt '%Y-%m-%dT%H:%M:%S' --format '%T|%w%f|%e' \
    -e attrib \
    -e close_write
    -e moved_to \
    -e moved_from \
    -e move_self \
    -e create \
    -e delete \
    -e delete_self \
    -e unmount \

    Events:
    access        file or directory contents were read
    modify        file or directory contents were written
    attrib        file or directory attributes changed
    close_write    file or directory closed, after being opened in
                   writable mode
    close_nowrite    file or directory closed, after being opened in
                   read-only mode
    close        file or directory closed, regardless of read/write mode
    open        file or directory opened
    moved_to    file or directory moved to watched directory
    moved_from    file or directory moved from watched directory
    move        file or directory moved to or from watched directory
    move_self        A watched file or directory was moved.
    create        file or directory created within watched directory
    delete        file or directory deleted within watched directory
    delete_self    file or directory was deleted
    unmount        file system containing file or directory unmounted

