#!/bin/sh
# sprawdza i/lub pobiera nowa wersje baz wirusow
# autorzy: Grzegorz Malicki i Dariusz Grzegorski
# wersja: 1.1  2004.06.22

# 1.1 poprawka czyszczenia, zmiana przekierowan skryptu
#     na zgodne z innymi shell'ami
#     '&>/dev/null' zastapione '>/dev/null 2>&1'

# WYMAGANE PROGRAMY POMOCNICZE: wget, md5sum (textutils), tr
# OPCJONALNE PROGRAMY POMOCNICZE: pgp, logger

# --------------------------------------------------------------
# PONIZSZE USTAWIENIA NALEZY DOSTOSOWAC DO LOKALNEJ KONFIGURACJI
# --------------------------------------------------------------

# pliki baz musz± byæ do odczytu przez mks
umask 022

# sciezka przeszukiwan
PATH=/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin
export PATH

# nazwa programu md5sum z pakietu GNU textutils
MD5SUM=md5sum
# w dystrybucji Debian jest md5sum.textutils
#MD5SUM=md5sum.textutils

# sciezka do programu mks32 (lub mks32.static)
MKS_XXXII=/usr/bin/mks32

# katalog z bazami wirusow
# /var/lib jest zgodny z File Hierarhy Standard 2.3
MKS_BASES=/var/lib/mks
#MKS_BASES=/usr/local/share/mks_vir

# katalog programu PGP, w ktorym znajduje sie klucz publiczny mks-a
# (zakomentuj, aby nie weryfikowac danych z serwera)
#PGP_PATH="${MKS_BASES}"/.pgp

# katalog, gdzie bazy beda sciagane i obrabiane (musi istniec)
#MKS_DOWNLOAD="${MKS_BASES}"/tmp
MKS_DOWNLOAD=/tmp

# czy wysylac sygnal do demona po wgraniu nowych baz?
MKSD_KICK=Y

# opcja (facility) logowania
MKS_LOG_FACILITY=daemon

# log z datami aktualizacji (zakomentuj, aby nie tworzyc logu)
MKS_UPDATE_LOG="${MKS_BASES}"/mks_vir_update.log

# plik tymczasowy
MKS_TMP_FILE="${MKS_DOWNLOAD}"/mkshttpdata

# URL do pliku startowego z linkiem do baz
MKS_START_URL=http://download.mks.com.pl/download/linux/bazy.link

#####################################
# dalej lepiej juz nie grzebac
#####################################

VERBOSE=N
USELOG=N

#####################################

cleanup ()
{
    rm -f "${MKS_TMP_FILE}" "${MKS_DOWNLOAD}"/wgetlist "${MKS_DOWNLOAD}"/copylist "${MKS_DOWNLOAD}"/mksbase?.dat
}

lecho ()
{
    if [ "${USELOG}" = "Y" ]
    then
        logger -p "${MKS_LOG_FACILITY}".$1 -t mksupdate -- "$2"
    else
	[ "$1" = err ] && echo "$2" >&2 || echo $
    fi
}

mkscheck ()
{
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Sprawdzam czy sa nowe bazy.
    fi
    
    rm -f "${MKS_TMP_FILE}"
    
    if ! wget -q -t 6 -O "${MKS_TMP_FILE}" "${MKS_START_URL}" >/dev/null 2>&1
    then
        lecho err "Nie mozna nawiazac polaczenia z serwerem glownym."
        return 2
    fi
    
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Polaczenie z serwerem glownym nawiazane.
    fi
    
    MKS_URL=`tr -d '\015' <"${MKS_TMP_FILE}"`
    rm -f "${MKS_TMP_FILE}"
    
    if ! wget -q -t 6 -O "${MKS_TMP_FILE}" "${MKS_URL}"bazy.md5 >/dev/null 2>&1
    then
        lecho err "Nie mozna nawiazac polaczenia z serwerem danych."
        return 3
    fi
    
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Polaczenie z serwerem danych nawiazane.
    fi
    
    if [ "${PGP_PATH}" != "" ]
    then
        if ! PGPPATH="${PGP_PATH}" pgp +force +batchmode "${MKS_TMP_FILE}" >/dev/null 2>&1
        then
            lecho err "Sygnatura PGP zweryfikowana niepoprawnie!"
            return 4
        elif [ "${VERBOSE}" = "Y" ]
        then
            echo Sygnatura PGP poprawna.
        fi
    fi
    
    rm -f "${MKS_DOWNLOAD}"/wgetlist
    
    grep mksbase.\\.dat "${MKS_TMP_FILE}" | tr -d '*\015' | \
    while read SUM NAME
    do
        if [ "$1" = "force" ]
        then
            echo "${MKS_URL}${NAME}" >>"${MKS_DOWNLOAD}"/wgetlist
        elif ! echo "${SUM} *${MKS_BASES}/${NAME}" | "${MD5SUM}" --status --check - >/dev/null 2>&1
        then
            echo "${MKS_URL}${NAME}" >>"${MKS_DOWNLOAD}"/wgetlist
        else
            echo "${MKS_BASES}/${NAME}" >>"${MKS_DOWNLOAD}"/copylist
        fi
    done
    
    if [ "$1" != "force" ]
    then
        if [ -s "${MKS_DOWNLOAD}"/wgetlist ]
        then
            lecho info "Sa dostepne nowe bazy wirusow."
            return 1
        else
            lecho info "Masz aktualne bazy."
            return 0
        fi
    else
        return 1
    fi
}

mksdoget ()
{
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Pobieram bazy
    fi
    
    if [ -s "${MKS_DOWNLOAD}"/copylist ]
    then
        while read COPYPATH
        do
            cp -f -p "${COPYPATH}" "${MKS_DOWNLOAD}"/ >/dev/null 2>&1
        done <"${MKS_DOWNLOAD}"/copylist
    fi
    
    ( cd "${MKS_DOWNLOAD}" ; wget -q -t 6 -i wgetlist >/dev/null 2>&1 )
    CHECKVAL=$?
    
    if [ ${CHECKVAL} -ne 0 ]
    then
        lecho err "Nie mozna nawiazac polaczenia z serwerem danych lub przerwana transmisja."
        return 5
    fi
    
    mksinstall
}

mksget ()
{
    mkscheck $1
    CHECKVAL=$?
    if [ ${CHECKVAL} -eq 1 ]
    then
        mksdoget
        CHECKVAL=$?
    fi
    return ${CHECKVAL}
}

mksinstall ()
{
    if [ ! -f "${MKS_DOWNLOAD}"/mksbase0.dat ]
    then
        lecho err "Brak sciagnietych baz na dysku."
        return 6
    fi
    
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Sprawdzam dzialanie mks-a
    fi
    
    if ! "${MKS_XXXII}" -f /dev/null --mks-vir-dat-path="${MKS_DOWNLOAD}"/ -s "${MKS_DOWNLOAD}"/mksbase0.dat >/dev/null 2>&1
    then
        lecho err "Blad formatu baz, sprawdz wersje mks-a."
        return 7
    fi
    
    if [ "${VERBOSE}" = "Y" ]
    then
        echo Instaluje
    fi
    
    if ! mv -f "${MKS_DOWNLOAD}"/mksbase?.dat "${MKS_BASES}"/
    then
        lecho err "Blad podczas instalacji baz."
        return 8
    fi
    
    if [ "${MKSD_KICK}" = "Y" -a -r /var/run/mksd/mksd.pid ]
    then
        if [ "${VERBOSE}" = "Y" ]
        then
            echo Wysylam SIGHUP procesowi mksd
        fi

        kill -HUP `cat /var/run/mksd/mksd.pid`
    fi
    
    if [ "${MKS_UPDATE_LOG}" != "" ]
    then
        date >>"${MKS_UPDATE_LOG}"
        if [ -s "${MKS_DOWNLOAD}"/wgetlist ]
        then
            cat "${MKS_DOWNLOAD}"/wgetlist >>"${MKS_UPDATE_LOG}"
        fi
        echo >>"${MKS_UPDATE_LOG}"
    fi
    
    lecho info "Nowe bazy zainstalowane."
    return 0
}

mkshelp ()
{
    lecho info "mksupdate wersja 0.32  (c) MkS Sp. z o.o. 2003,2004"
    lecho info ""
    lecho info "skladnia: mksupdate opcja [verbose|uselog]"
    lecho info ""
    lecho info "opcje:"
    lecho info "   check    :sprawdza czy sa nowe bazy"
    lecho info "   get      :pobiera nowe bazy jesli trzeba i instaluje"
    lecho info "   getforce :pobiera bazy bez sprawdzania czy to potrzebne i instaluje"
    lecho info "   install  :sama instalacja (jesli bazy pobrane recznie)"
    lecho info "   help     :ten opis"
    lecho info ""
    lecho info "na koncu mozna dodac verbose to wtedy bedzie widac co sie dzieje"
    lecho info "opcja uselog przekierowuje stdout do logow systemowych"
}


if [ "$2" = "verbose" ]
then
    VERBOSE=Y
fi

if [ "$2" = "uselog" ]
then
    USELOG=Y
fi

case "$1" in
help)
    mkshelp
    ;;
check)
    cleanup
    mkscheck noforce
    cleanup
    ;;
get)
    cleanup
    mksget noforce
    cleanup
    ;;
getforce)
    cleanup
    mksget force
    cleanup
    ;;
install)
    mksinstall
    ;;
*)
    mkshelp
    ;;
esac

exit 0
