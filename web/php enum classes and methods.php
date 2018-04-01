<?php


ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

foreach(get_declared_classes() as $classname)
{
    echo $classname;
    print_r(get_class_methods($classname));
}
    


print_r(get_defined_functions());
?>