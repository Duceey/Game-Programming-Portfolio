using UnityEngine;
using UnityEngine.SceneManagement;


public class LevelSelect : MonoBehaviour
{
    public int LevelIndex;
    public int BufferIndex = 2;

    public void GoToLevel()
    {
        SceneManager.LoadScene(LevelIndex + BufferIndex);
    }
}
