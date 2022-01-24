using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class WorldSelectControl : MonoBehaviour
{

    public Button world2Button, world3Button;
    int worldComplete;

    void Start()
    {
        worldComplete = PlayerPrefs.GetInt("WorldComplete");
        world2Button.interactable = false;
        world3Button.interactable = false;

        switch (worldComplete)
        {
            case 1:
                world2Button.interactable = true;
                break;
            case 2:
                world2Button.interactable = true;
                world3Button.interactable = true;
                break;
        }
    }

    public void levelToLoad (int level)
    {
        SceneManager.LoadScene(level);
    }

    // Currently not Implemented
    public void resetPlayerPrefs()
    {
        world2Button.interactable = false;
        world3Button.interactable = false;
        PlayerPrefs.DeleteAll();
    }

}
