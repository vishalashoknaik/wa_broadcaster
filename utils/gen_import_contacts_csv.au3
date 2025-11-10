#include <array.au3>
#include <file.au3>


;CSV format for contacts
; output csv array oc
;Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,IM 1 - Type,IM 1 - Service,IM 1 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value,Phone 3 - Type,Phone 3 - Value,Address 1 - Type,Address 1 - Formatted,Address 1 - Street,Address 1 - City,Address 1 - PO Box,Address 1 - Region,Address 1 - Postal Code,Address 1 - Country,Address 1 - Extended Address,Organization 1 - Type,Organization 1 - Name,Organization 1 - Yomi Name,Organization 1 - Title,Organization 1 - Department,Organization 1 - Symbol,Organization 1 - Location,Organization 1 - Job Description,Website 1 - Type,Website 1 - Value,Website 2 - Type,Website 2 - Value,Website 3 - Type,Website 3 - Value,Website 4 - Type,Website 4 - Value,Custom Field 1 - Type,Custom Field 1 - Value
; First Second,First ,,second,,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile,+91 9999999999,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
;	oc0,oc1,,oc2,,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile,oc3,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


$csv_header = 'Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,IM 1 - Type,IM 1 - Service,IM 1 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value,Phone 3 - Type,Phone 3 - Value,Address 1 - Type,Address 1 - Formatted,Address 1 - Street,Address 1 - City,Address 1 - PO Box,Address 1 - Region,Address 1 - Postal Code,Address 1 - Country,Address 1 - Extended Address,Organization 1 - Type,Organization 1 - Name,Organization 1 - Yomi Name,Organization 1 - Title,Organization 1 - Department,Organization 1 - Symbol,Organization 1 - Location,Organization 1 - Job Description,Website 1 - Type,Website 1 - Value,Website 2 - Type,Website 2 - Value,Website 3 - Type,Website 3 - Value,Website 4 - Type,Website 4 - Value,Custom Field 1 - Type,Custom Field 1 - Value'
; input csv array c
; First Name,	Tag,	Second Name,	Tag,	Additinal Tag,	Name Prefix, Prefix,  Phone Number
;   c0			c1			c2			c3			c4				c5        c6        c7
; TO DO:
; Process input array
; Merge c5 _ c0 and c1      first_name
; Merge c2 c3 and c4   sec_name
; Merge c6 and c7	   ph_num
; Create output array
; oc0 --> Merge c01 and c234 with space
; oc1 --> c01
; oc2 --> c234
; oc3 --> c56


Global $in_csv_arr, $old_csv_arr ;

;$input_csv = 'C:\Users\naikvis\Downloads\Import_Google - Sheet1.csv';
$default_in_csv = @ScriptDir & "\contact_export_in.csv" ;
$input_csv = InputBox("Enter input CSV", "Enter CSV file generated in specified input format", $default_in_csv) ;
;$input_csv = 'C:\Users\naikvis\Downloads\Import_Google - Sheet1(5).csv'

_FileReadToArray($input_csv, $in_csv_arr, 1, ",") ;

$output_csv = $input_csv & '_out.csv' ;
_ArrayDisplay($in_csv_arr)


;write header into output file
FileDelete($output_csv) ;
;MsgBox(0,0,0)
FileWriteLine($output_csv, $csv_header)


$prefix_in = InputBox("Input prefix", "", "") ;
$old_csv = @ScriptDir & '\' & $prefix_in & '.csv' ;

; If the old file is not present then we need to generate it
;It means we have to write the header also
If Not FileExists($old_csv) Then
	FileWriteLine($old_csv, $csv_header)
EndIf

Local $old_csv_arr;
_FileReadToArray($old_csv, $old_csv_arr, 1, ",") ;
;_ArrayDisplay($old_csv_arr)
;MsgBox(0,@error,$old_csv_arr[0])
$old_cnt = $old_csv_arr[0][0]-1;
;MsgBox(0,$old_cnt,$old_csv_arr[0][0])

For $i = 2 To $in_csv_arr[0][0] ; skip first line. It contains header

	$prefix = $prefix_in & StringFormat("%03d", $i - 1) ;

	$c01 = $in_csv_arr[$i][0] & ' ' & $in_csv_arr[$i][1] ;
	$c234 = $in_csv_arr[$i][2] & ' ' & $in_csv_arr[$i][3] & ' ' & $in_csv_arr[$i][4] ;		; add a space for additioanal tag
	$c5 = $in_csv_arr[$i][5]
	$ph_num = $in_csv_arr[$i][6] & $in_csv_arr[$i][7] ;
	$ph_num2 = $in_csv_arr[$i][8] & $in_csv_arr[$i][9] ;

	$mobile2_lable = ""
	If Not ($ph_num2 = "") Then
		$mobile2_lable = "Mobile2" ;
	EndIf


	;MsgBox(0,0,$ph_num);
	$oc0 = $c5 & " " & $c01 & ' ' & $c234 ;
	$oc1 = $prefix & $c5 & " " & $c01 ;
	$oc2 = $c234 ;

	; now write line by line
	;	oc0,oc1,,oc2,,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile,oc3,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

	$line = $oc0 & "," & $oc1 & ",," & $oc2 & ",,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile," & $ph_num & ',' & $mobile2_lable & ',' & $ph_num2 & ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
	FileWriteLine($output_csv, $line)

	If (_ArraySearch($old_csv_arr, $ph_num) > -1) Then
		ContinueLoop ;
	EndIf
	If (_ArraySearch($old_csv_arr, $oc0) > -1) Then
		ContinueLoop ;
	EndIf

	$prefix = $prefix_in & StringFormat("%03d", $i - 1+$old_cnt) ;
	$oc0 = $c5 & " " & $c01 & ' ' & $c234 ;
	$oc1 = $prefix & $c5 & " " & $c01 ;
	$oc2 = $c234 ;

	; now write line by line
	;	oc0,oc1,,oc2,,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile,oc3,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

	$line = $oc0 & "," & $oc1 & ",," & $oc2 & ",,,,,,,,,,,,,,,,,,,,,,,* My Contacts,,,,,,,,Mobile," & $ph_num & ',' & $mobile2_lable & ',' & $ph_num2 & ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
	FileWriteLine($output_csv, $line)



	If (_ArraySearch($old_csv_arr, $prefix) > -1) Then
		MsgBox(0,'Warning','Prefix already exists!!');
	EndIf


	FileWriteLine($old_csv, $line)
	;MsgBox(0,0,$line)
Next

