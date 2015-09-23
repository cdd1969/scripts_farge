if __name__ == '__main__':

    MThw   =  2.28  # [mAMSL]
    MTnw   = -1.57  # [mAMSL]
    NNTnw  = -3.42  # [mAMSL]
    HThw   =  4.99  # [mAMSL]
    MSpTnw = -1.87  # [mAMSL]

    # Bild E 19-2, EAU 2012
    print "# ------------------------------------------"
    print "# 3a) Persistent Design Situation"
    print "# ------------------------------------------"
    a = 0.5*(MThw - MTnw)
    d = MTnw - MSpTnw
    dh = a + 0.3 + d  #[m]

    print '\twaterlevel at MSpTnw = ', MSpTnw, '[mAMSL]'
    print '\tdh = {0:.2f} m'.format(dh)

    print "# ------------------------------------------"
    print "# 3b) Accidental Design Situation"
    print "# Grenzfall extremer Niedrig-wasserstand"
    print "# ------------------------------------------"
    a = 0.5*(MThw - MTnw)
    b = 0.5*(MSpTnw - NNTnw)
    d = MTnw - MSpTnw
    dh = a + 2*b + d  #[m]

    print '\twaterlevel at NNTnw = ', NNTnw, '[mAMSL]'
    print '\tdh = {0:.2f} m'.format(dh)

    print "# ------------------------------------------"
    print "# 3c) Accidental Design Situation"
    print "# Grenzfall abfliessendes Hochwasser"
    print "# ------------------------------------------"
    a = 0.5*(MThw - MTnw)
    dh = 0.3 + 2*a  #[m]

    print '\twaterlevel at MTnw = ', MTnw, '[mAMSL]'
    print '\tdh = {0:.2f} m'.format(dh)
