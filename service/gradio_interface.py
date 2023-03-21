import os
import gradio as gr
from space_filler.space_addity import SpaceAddity


base_dir = os.path.abspath(os.path.join(__file__, "../../data"))
word_dict_path = os.path.join(base_dir, 'word_probs.json')
filler = SpaceAddity(word_dict_path)


def gradio_filler(text, simplified_mode):
    """
    The main function to wrap gradio interface
    Args:
        text: (str) input string (with missed spaces, [opt.])
        simplified_mode: (bool) word split mode

    Returns:
        Gradio interface outputs
    """
    global filler
    assert len(text) < 512, \
        f'Text length exceeds allowed limit (512). Remove {len(text) - 511} characters.'
    filler.simplified_mode = simplified_mode
    split_text, indices = filler.add_spaces(text)

    return split_text, indices


# Custom gradio web interface for FastAPI app
gradio_interface = gr.Interface(fn=gradio_filler,
                                inputs=[gr.Textbox(label="INPUT SENTENCE", placeholder=""),
                                        gr.Checkbox(label="SIMPLIFIED MODE")],
                                outputs=[gr.Textbox(label="CORRECTED SENTENCE"),
                                         gr.Text(label="SPACE POSITIONS")],
                                allow_flagging="never",
                                title="Space Filler",
                                examples=[["Groundcontrol to Mr.Dot", True],
                                          ["Searchbar is acompoundword", True],
                                          ["Searchbar is acompoundword", False],
                                          ["Seeyoulater,innovator!", False]],
                                )
