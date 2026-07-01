"""Development entrypoint for Buvette Manager."""

from app import create_app

app = create_app()


def print_startup_banner() -> None:
    """Display readable startup information for local and Docker runs."""

    print("\n=== Buvette Manager Startup ===")
    print(f"Application Name: {app.config.get('APP_NAME', 'Buvette Manager')}")
    print(f"Environment: {app.config.get('ENVIRONMENT')}")
    print(f"Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print("Listening Address: http://0.0.0.0:5000")
    print(f"Loaded Blueprints: {', '.join(sorted(app.blueprints.keys()))}")
    print("================================\n", flush=True)


if __name__ == "__main__":
    print_startup_banner()
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", True))
