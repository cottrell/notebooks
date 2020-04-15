https://unix.stackexchange.com/questions/143864/monitor-all-login-attempts

/etc/rsyslog.d/ommail.conf

$ModLoad ommail
$ActionMailSMTPServer localhost
$ActionMailFrom bleepblop
$ActionMailTo david.cottrell@gmail.com
$template mailSubject,"Login Alert on %hostname%"
$template mailBody,"\n\n%msg%"
$ActionMailSubject mailSubject
$ActionExecOnlyOnceEveryInterval 1
# the if ... then ... mailBody mus be on one line!
if $msg contains 'session opened for user' then :ommail:;mailBody
