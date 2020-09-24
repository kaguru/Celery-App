from tasks import add


def operator():
    result = add.delay(4, 4)
    result_is_ready_before_get = result.ready()
    result_get = result.get()
    result_is_ready_after_get_ready = result.ready()

    print(f"""
    RESULT:: {result}
    RESULT IS READY BEFORE GET:: {result_is_ready_before_get}
    RESULT GET:: {result_get}
    RESULT IS READY AFTER GET:: {result_is_ready_after_get_ready}
    """)


if __name__ == "__main__":
    operator()
