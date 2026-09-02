import subprocess
import sys


def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python scripts/run_audit.py https://example.com"
        )

        sys.exit(1)

    website = sys.argv[1]

    print(
        "\nStarting website audit..."
    )

    subprocess.run([

        sys.executable,

        "scripts/crawler.py",

        website

    ])

    print(
        "\nRunning technical audit..."
    )

    subprocess.run([

        sys.executable,

        "scripts/technical_audit.py"

    ])

    print(
        "\nAudit data generated successfully."
    )

    print(
        "\nNow ask Claude to analyze the data "
        "and generate the final report."
    )


if __name__ == "__main__":

    main()
