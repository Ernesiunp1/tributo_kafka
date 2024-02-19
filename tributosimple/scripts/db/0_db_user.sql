/*----------------------------------------------------------------------------
 User access
 -----------------------------------------------------------------------------*/
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'passw0rd';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'passw0rd';