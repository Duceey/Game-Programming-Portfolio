using UnityEngine;
using UnityEngine.SceneManagement;

public class ExitGame : MonoBehaviour
{
    public void Exit()
    {
        SceneManager.LoadScene(0);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Exit(); // Later will pull up a menu
        }
    }
}
