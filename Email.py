import smtplib

Email = "myimpactmeter@gmail.com"
Password = "my1234my"


def SuccessfulDonation(email, name, amount, inarea):
    try:
        Email = "myimpactmeter@gmail.com"
        Password = "my1234my"

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(Email, Password)

            subject = "Thanks For Donation"
            body = (
                "Hi "
                + str(name)
                + "!\n\nThanks For Donating "
                + str(amount)
                + " $ for "
                + str(inarea)
                + "\n\nMy Impact Meter will make sure your Donation will go in Right Hands. \n\nThis is Automated Message Don't Reply For any Query Contact us at mcheema2010@gmail.com"
            )
            msg = f"Subject:{subject}\n\n{body}"
            smtp.sendmail(Email, email, msg)
    except:
        SuccessfulDonation(email, name, amount, inarea)

