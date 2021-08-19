update queries SET tags=array_remove(tags,'for_each_metrics');
update queries SET tags=array_remove(tags,'for_message');